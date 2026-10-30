"""Analysis 1C calendar alignment, paired arithmetic, metadata and presentation."""

from copy import deepcopy
import json
import subprocess
import sys
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from bondview import TreasuryMarketAnalysis
from bondview.analysis.scenarios import CHANGE_COLUMNS, ScenarioSet, build_conditional_scenarios
from bondview.plotting.scenarios import plot_scenarios
from test_treasury_curve import example_frame


def dated_frame(dates, values=None):
    """Synthetic observed dates with hand-checkable percent levels, not market data."""
    dates = pd.to_datetime(dates)
    days = (dates - dates[0]).days.to_numpy()
    if values is None:
        values = np.column_stack([4 + days * .002, 4.5 - days * .001, 5 + days * .003])
    data = pd.DataFrame(values, index=dates, columns=['DGS2', 'DGS10', 'DGS30'])
    data.index.name = 'date'
    data.attrs['metadata'] = deepcopy(example_frame().attrs['metadata'])
    for info in data.attrs['metadata'].values():
        info['source'] = 'Synthetic scenario fixture, not market data'
    return data


def scenario_frame():
    """Weekday observations across a leap year, with small six-month 10Y changes."""
    return dated_frame(pd.bdate_range('2024-01-01', '2024-12-31'))


def singleton_frame():
    return dated_frame(['2024-01-31', '2024-07-31'],
                       [[4.1, 4.6, 5.1], [4.3, 4.35, 5.6]])


def build(data=None, **kwargs):
    options = dict(condition_tenor='DGS10', lower_bp=-1000, upper_bp=1000)
    options.update(kwargs)
    return build_conditional_scenarios(scenario_frame() if data is None else data, **options)


class ScenarioTests(unittest.TestCase):
    def test_default_six_months_complete_joint_vectors_and_inclusive_bounds(self):
        data = singleton_frame()
        before = data.copy(deep=True)
        result = build(data, lower_bp=-25, upper_bp=-25)
        self.assertIsInstance(result, ScenarioSet)
        row = result.scenarios.iloc[0]
        self.assertEqual(len(result.scenarios), 1)
        self.assertEqual(row.scenario_id, 'UST_20240131_20240731')
        self.assertEqual(row.start_date, pd.Timestamp('2024-01-31'))
        self.assertEqual(row.end_date, pd.Timestamp('2024-07-31'))
        self.assertEqual(row.elapsed_days, 182)
        np.testing.assert_allclose(row[list(CHANGE_COLUMNS)].astype(float), [20, -25, 50])
        self.assertEqual(result.metadata['horizon_months'], 6)
        self.assertEqual(result.metadata['sampling'], 'monthly')
        self.assertEqual(result.metadata['max_shortfall_days'], 7)
        self.assertEqual(result.metadata['condition'], {'tenor':'DGS10', 'lower_bp':-25., 'upper_bp':-25., 'inclusive':True})
        pd.testing.assert_frame_equal(data, before)
        self.assertTrue(build(data, lower_bp=-24.999, upper_bp=-24.999).scenarios.empty)
        self.assertIn('not independent', result.metadata['interpretation'])

    def test_monthly_sequence_uses_original_latest_anchor_not_month_ends(self):
        data = dated_frame(pd.bdate_range('2026-01-01', '2026-10-26'))
        result = build(data)
        rows = result.scenarios
        self.assertEqual(rows.target_end_date.tolist(), list(pd.to_datetime(
            ['2026-10-26', '2026-09-26', '2026-08-26', '2026-07-26'])))
        self.assertEqual(rows.target_start_date.tolist(), list(pd.to_datetime(
            ['2026-04-26', '2026-03-26', '2026-02-26', '2026-01-26'])))
        self.assertEqual(rows.start_date.tolist(), list(pd.to_datetime(
            ['2026-04-27', '2026-03-26', '2026-02-26', '2026-01-26'])))
        self.assertEqual(rows.end_date.tolist(), list(pd.to_datetime(
            ['2026-10-26', '2026-09-25', '2026-08-26', '2026-07-24'])))
        self.assertEqual(result.metadata['sampling_anchor'], '2026-10-26')
        self.assertEqual(result.metadata['counts']['intended_windows'], 4)
        self.assertEqual(result.metadata['end_convention'], 'latest_complete_date_minus_integer_calendar_months')

    def test_six_calendar_months_clip_leap_years_without_anchor_drift(self):
        for year, feb_end in ((2024, '2024-02-29'), (2025, '2025-02-28')):
            with self.subTest(year=year):
                result = build(dated_frame(pd.bdate_range(f'{year}-01-01', f'{year}-12-31')))
                rows = result.scenarios
                # Each end is offset from December 31, so November's clipping
                # must not cause October or August to drift to the 30th.
                self.assertEqual(rows.target_end_date.dt.day.tolist(), [31, 30, 31, 30, 31, 31])
                august = rows.loc[rows.target_end_date == pd.Timestamp(f'{year}-08-31')].iloc[0]
                self.assertEqual(august.target_start_date, pd.Timestamp(feb_end))
                self.assertEqual(august.start_date, pd.Timestamp(feb_end))
                self.assertEqual(august.target_end_date - august.target_start_date,
                                 pd.Timedelta(days=184))

    def test_combined_shortfall_boundary_and_no_outside_search(self):
        for start, accepted in (('2026-03-29', True), ('2026-03-30', False)):
            with self.subTest(actual_start=start):
                # Second intended window: March 26 to September 26.
                # Nearby dates outside either boundary must remain excluded.
                data = dated_frame(['2026-03-20', '2026-03-25', start,
                                    '2026-09-22', '2026-09-27', '2026-10-26'])
                result = build(data)
                rows = result.scenarios
                self.assertEqual(len(rows), int(accepted))
                self.assertEqual(result.metadata['counts']['shortfall_excluded'], 1 if accepted else 2)
                if accepted:
                    row = rows.iloc[0]
                    self.assertEqual((row.start_date, row.end_date),
                                     (pd.Timestamp(start), pd.Timestamp('2026-09-22')))
                    self.assertEqual(row.shortfall_days, 7)  # Three + four days.
                    self.assertEqual(row.target_start_date, pd.Timestamp('2026-03-26'))
                    self.assertEqual(row.target_end_date, pd.Timestamp('2026-09-26'))
                    for sampling in ('daily', 'monthly'):
                        other = build(data, sampling=sampling)
                        self.assertTrue((other.scenarios.shortfall_days <= 7).all())

    def test_boundary_missing_yields_use_only_complete_inside_dates(self):
        data = dated_frame(pd.bdate_range('2026-01-01', '2026-10-26'))
        # For the second monthly window March 26 to September 26,
        # reject incomplete March 26 and September 25 endpoints.
        data.loc['2026-03-26', 'DGS2'] = np.nan
        data.loc['2026-09-25', 'DGS30'] = np.nan
        result = build(data)
        row = result.scenarios.iloc[1]
        self.assertEqual(row.start_date, pd.Timestamp('2026-03-27'))
        self.assertEqual(row.end_date, pd.Timestamp('2026-09-24'))
        self.assertEqual(row.shortfall_days, 3)
        self.assertEqual(result.metadata['counts']['incomplete_rows_excluded'], 2)
        self.assertFalse(result.scenarios[list(CHANGE_COLUMNS)].isna().any().any())

    def test_interior_missing_observations_do_not_invalidate_window(self):
        data = singleton_frame()
        before = build(data)
        data = data.reindex(pd.to_datetime(['2024-01-31', '2024-03-15', '2024-05-20', '2024-07-31']))
        data.loc['2024-03-15'] = [4.0, np.nan, 4.9]
        result = build(data)
        pd.testing.assert_frame_equal(before.scenarios, result.scenarios)
        self.assertEqual(result.metadata['counts']['incomplete_rows_excluded'], 2)

    def test_daily_uses_every_complete_end_newest_first_and_same_safeguard(self):
        data = scenario_frame()
        data.loc['2024-12-30', 'DGS2'] = np.nan
        result = build(data, sampling='daily')
        common_ends = data.dropna().index
        expected_ends = [d for d in common_ends[::-1]
                         if d - pd.DateOffset(months=6) >= common_ends[0]]
        self.assertEqual(result.scenarios.target_end_date.tolist(), expected_ends)
        self.assertEqual(result.scenarios.end_date.tolist(), expected_ends)
        self.assertTrue((result.scenarios.shortfall_days <= 7).all())
        self.assertTrue(result.scenarios.target_end_date.is_monotonic_decreasing)
        self.assertGreater(len(result.scenarios), len(build(data).scenarios))
        # A daily end remains excluded when its only in-window start is 19 days late.
        sparse = dated_frame(['2026-01-01', '2026-05-15', '2026-10-26'])
        self.assertTrue(build(sparse, sampling='daily').scenarios.empty)
        self.assertGreater(build(sparse, sampling='daily').metadata['counts']['shortfall_excluded'], 0)

    def test_daily_accepts_seven_day_start_shortfall_but_rejects_eight(self):
        for first_inside, expected in (('2026-05-03', 1), ('2026-05-04', 0)):
            with self.subTest(first_inside=first_inside):
                data = dated_frame(['2026-01-01', '2026-04-25', first_inside, '2026-10-26'])
                result = build(data, sampling='daily')
                self.assertEqual(len(result.scenarios), expected)
                if expected:
                    self.assertEqual(result.scenarios.iloc[0].shortfall_days, 7)
                    self.assertEqual(result.scenarios.iloc[0].start_date, pd.Timestamp(first_inside))

    def test_every_vector_matches_independent_inside_window_enumeration(self):
        data = scenario_frame()
        monthly_ends = pd.to_datetime(['2024-12-31', '2024-11-30', '2024-10-31',
                                       '2024-09-30', '2024-08-31', '2024-07-31'])
        for sampling in ('daily', 'monthly'):
            result = build(data, condition_tenor='DGS2', lower_bp=36.4, upper_bp=36.6, sampling=sampling)
            ends = data.index[::-1] if sampling == 'daily' else monthly_ends
            expected = []
            for end in ends:
                start = end - pd.DateOffset(months=6)
                if start < data.index[0]:
                    continue
                inside = [d for d in data.index if start <= d <= end]
                if len(inside) < 2:
                    continue
                first, last = inside[0], inside[-1]
                if (end - start).days - (last - first).days > 7:
                    continue
                changes = (data.loc[last] - data.loc[first]) * 100
                if 36.4 <= round(changes.DGS2, 10) <= 36.6:
                    expected.append((first, last, changes))
            self.assertGreater(len(expected), 0)
            self.assertEqual(len(result.scenarios), len(expected))
            for row, (first, last, changes) in zip(result.scenarios.itertuples(), expected):
                self.assertEqual((row.start_date, row.end_date), (first, last))
                np.testing.assert_allclose([getattr(row,c) for c in CHANGE_COLUMNS], changes, atol=1e-10)

    def test_insufficient_windows_excluded_and_count_accounting(self):
        data = dated_frame(['2025-12-01', '2026-01-01', '2026-08-01'])
        result = build(data)
        counts = result.metadata['counts']
        self.assertTrue(result.scenarios.empty)
        self.assertEqual(counts['intended_windows'], 3)
        self.assertEqual(counts['insufficient_observations_excluded'], 2)
        self.assertEqual(counts['shortfall_excluded'], 1)
        for sampling in ('daily', 'monthly'):
            counts = build(sampling=sampling).metadata['counts']
            self.assertEqual(counts['intended_windows'], counts['eligible_windows'] +
                             counts['insufficient_observations_excluded'] + counts['shortfall_excluded'])

    def test_reference_bounds_control_latest_anchor_and_oldest_complete_window(self):
        data = scenario_frame()
        data.loc['2024-01-01', 'DGS30'] = np.nan
        result = build(data, reference_start='2024-01-01', reference_end='2024-11-30')
        self.assertEqual(result.metadata['reference'], dict(requested_start='2024-01-01',
                         requested_end='2024-11-30', effective_start='2024-01-02', effective_end='2024-11-29'))
        self.assertEqual(result.metadata['sampling_anchor'], '2024-11-29')
        self.assertEqual(result.scenarios.target_end_date.dt.day.tolist(), [29]*5)
        self.assertTrue((result.scenarios.target_start_date >= pd.Timestamp('2024-01-02')).all())
        self.assertEqual(build(data).metadata['counts']['reference_rows'], len(data)-1)
        self.assertEqual(build(data).metadata['counts']['incomplete_rows_excluded'], 0)
        with self.assertRaisesRegex(ValueError, 'No complete'):
            build(data, reference_start='2025-01-01')

    def test_ids_reproducible_across_bounds_order_and_source_mutation(self):
        data=scenario_frame()
        result=build(data)
        reverse=build(data.iloc[::-1])
        pd.testing.assert_frame_equal(result.scenarios,reverse.scenarios)
        selected=build(data,lower_bp=-18.3,upper_bp=-18.3)
        self.assertIn(selected.scenarios.iloc[0].scenario_id,result.scenarios.scenario_id.tolist())
        self.assertTrue(result.scenarios.scenario_id.is_unique)
        source=deepcopy(result.metadata['provenance'])
        data.attrs['metadata']['DGS2']['source']='changed'
        self.assertEqual(result.metadata['provenance'],source)
        json.dumps(result.metadata,allow_nan=False)

    def test_empty_set_and_short_history_preserve_schema_summary_and_plot(self):
        for result in (build(lower_bp=900,upper_bp=901), build(horizon_months=120),
                       build(scenario_frame().iloc[:1])):
            self.assertTrue(result.scenarios.empty)
            self.assertEqual(list(result.scenarios.columns), ['scenario_id','start_date','target_end_date','end_date','elapsed_days',*CHANGE_COLUMNS,'target_start_date','shortfall_days'])
            self.assertEqual(result.summary().shape,(3,5))
            self.assertTrue(result.summary().isna().all().all())
            self.assertIsNotNone(plot_scenarios(result))
            with patch('IPython.display.display') as display:
                result.show_summary()
                self.assertEqual(display.call_count,3)

    def test_summary_hand_calculated_marginals(self):
        frame=pd.DataFrame({c:[-20.,20.] for c in CHANGE_COLUMNS})
        result=ScenarioSet(frame,{})
        np.testing.assert_allclose(result.summary().to_numpy(),[[-20,-16,0,16,20]]*3)
        self.assertEqual(result.summary().index.tolist(),['DGS2','DGS10','DGS30'])
        singleton=build(singleton_frame(),lower_bp=-25,upper_bp=-25)
        np.testing.assert_allclose(singleton.summary().to_numpy(),[[20]*5,[-25]*5,[50]*5])

    def test_invalid_parameters_and_observation_contract(self):
        for options in ({'condition_tenor':'DGS30'}, {'lower_bp':1,'upper_bp':0},
                        {'lower_bp':np.nan},{'upper_bp':np.inf},{'lower_bp':'0'}, {'lower_bp':True},
                        {'horizon_months':0},{'horizon_months':-1},{'horizon_months':1.5},
                        {'horizon_months':True},{'sampling':'weekly'},
                        {'reference_start':'2025-02-01','reference_end':'2024-01-01'},
                        {'reference_start':'2024/01/01'}, {'reference_end':pd.NaT}):
            with self.subTest(options=options),self.assertRaises(ValueError):
                build(**options)
        for data in (scenario_frame().drop(columns='DGS30'),scenario_frame()*np.nan):
            with self.assertRaises(ValueError):build(data)
        data=scenario_frame()
        data.attrs['metadata']['DGS2']['units']='Decimal'
        with self.assertRaisesRegex(ValueError,'daily Percent'):build(data)
        data=scenario_frame()
        meta=data.attrs.pop('metadata')
        with self.assertRaises(ValueError):build(data)
        self.assertFalse(build(data,metadata=meta).scenarios.empty)

    def test_facade_plot_axes_hover_and_display_without_rebuilding(self):
        for tenor,x in (('DGS10','DGS2'),('DGS2','DGS10')):
            result=TreasuryMarketAnalysis(scenario_frame()).scenarios(condition_tenor=tenor, lower_bp=-1000,upper_bp=1000,horizon_months=1)
            before=result.scenarios.copy(deep=True)
            figure=plot_scenarios(result)
            trace=figure.data[0]
            np.testing.assert_array_equal(trace.x,result.scenarios[f'{x}_change_bp'])
            np.testing.assert_array_equal(trace.y,result.scenarios.DGS30_change_bp)
            np.testing.assert_array_equal(trace.marker.color,result.scenarios[f'{tenor}_change_bp'])
            self.assertIn('(bp)',figure.layout.xaxis.title.text)
            for text in ('Historical start','Historical end','Elapsed days','Calendar target'):
                self.assertIn(text,trace.hovertemplate)
            with patch('bondview.analysis.scenarios.build_conditional_scenarios',side_effect=AssertionError('rebuild')), \
                 patch('plotly.graph_objects.Figure.show') as show,patch('IPython.display.display'):
                result.show_plot()
                result.show_summary()
            show.assert_called_once()
            pd.testing.assert_frame_equal(result.scenarios,before)

    def test_numerical_use_does_not_import_visualization(self):
        code='''
import sys
from bondview.analysis.scenarios import ScenarioSet, build_conditional_scenarios
assert 'bondview.market' not in sys.modules
assert not any(m.startswith(('plotly','bondview.plotting','bondview.presentation')) for m in sys.modules)
'''
        subprocess.run([sys.executable,'-c',code],check=True)
