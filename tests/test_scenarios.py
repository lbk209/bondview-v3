"""Analysis 1C calendar alignment, paired arithmetic, metadata and presentation."""

from copy import deepcopy
import inspect
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
        self.assertEqual(result.metadata['sampling_step_observations'], 1)
        self.assertEqual(result.metadata['max_shortfall_days'], 7)
        self.assertEqual(result.metadata['condition'], {'tenor':'DGS10', 'lower_bp':-25., 'upper_bp':-25., 'inclusive':True})
        pd.testing.assert_frame_equal(data, before)
        self.assertTrue(build(data, lower_bp=-24.999, upper_bp=-24.999).scenarios.empty)
        self.assertIn('not independent', result.metadata['interpretation'])

    def test_public_defaults_and_removed_sampling_parameter(self):
        for function in (build_conditional_scenarios, TreasuryMarketAnalysis.scenarios):
            params = inspect.signature(function).parameters
            self.assertEqual(params['sampling_step_observations'].default, 1)
            self.assertNotIn('sampling', params)
        direct = build()
        explicit = build(sampling_step_observations=1)
        facade = TreasuryMarketAnalysis(scenario_frame()).scenarios(
            condition_tenor='DGS10', lower_bp=-1000, upper_bp=1000)
        pd.testing.assert_frame_equal(direct.scenarios, explicit.scenarios)
        pd.testing.assert_frame_equal(direct.scenarios, facade.scenarios)

    def test_step_one_preserves_hand_checked_previous_daily_vectors_and_order(self):
        data = dated_frame(['2024-01-31', '2024-02-29', '2024-07-31',
                            '2024-08-29', '2024-08-30', '2024-09-30'],
                           [[4.1,4.6,5.1], [4.2,4.7,5.2], [4.3,4.35,5.6],
                            [4.4,4.8,5.1], [4.5,4.95,5.4], [4.6,4.9,5.3]])
        result = build(data, lower_bp=-25, upper_bp=25)
        rows = result.scenarios
        self.assertEqual(rows.scenario_id.tolist(), ['UST_20240229_20240830',
                         'UST_20240229_20240829', 'UST_20240131_20240731'])
        np.testing.assert_allclose(rows[list(CHANGE_COLUMNS)], [[30,25,20], [20,10,-10], [20,-25,50]])
        self.assertEqual(rows.start_date.tolist(), list(pd.to_datetime(['2024-02-29', '2024-02-29', '2024-01-31'])))
        self.assertEqual(rows.end_date.tolist(), list(pd.to_datetime(['2024-08-30', '2024-08-29', '2024-07-31'])))
        self.assertEqual(rows.shortfall_days.tolist(), [0,0,0])
        self.assertEqual(result.metadata['sampling_anchor'], '2024-07-31')
        self.assertNotIn('sampling', result.metadata)
        self.assertTrue(rows.end_date.is_monotonic_decreasing)

    def test_steps_five_twenty_count_complete_candidates_from_oldest(self):
        data = scenario_frame()
        data.loc['2024-07-03', 'DGS10'] = np.nan
        data.loc['2024-07-04'] = np.nan
        candidates = data.dropna().index[data.dropna().index >= pd.Timestamp('2024-07-01')]
        for step, second in ((5, '2024-07-10'), (20, '2024-07-31')):
            with self.subTest(step=step):
                result = build(data, sampling_step_observations=step)
                expected = candidates[::step][::-1]
                self.assertEqual(result.scenarios.target_end_date.tolist(), list(expected))
                oldest = result.scenarios.iloc[::-1]
                self.assertEqual(oldest.iloc[0].target_end_date, pd.Timestamp('2024-07-01'))
                self.assertEqual(oldest.iloc[1].target_end_date, pd.Timestamp(second))
                self.assertEqual(result.metadata['sampling_anchor'], '2024-07-01')
                counts = result.metadata['counts']
                self.assertEqual(counts['candidate_endpoints'], len(candidates))
                self.assertEqual(counts['sampled_endpoints'], len(expected))
                self.assertEqual(counts['intended_windows'], len(expected))
        self.assertNotEqual((pd.Timestamp('2024-07-10') - pd.Timestamp('2024-07-01')).days, 5)

    def test_later_observations_preserve_previously_sampled_endpoints_and_vectors(self):
        before_data = scenario_frame()
        extended = dated_frame(pd.bdate_range('2024-01-01', '2025-01-31'))
        for step in (1, 5, 20):
            before = build(before_data, sampling_step_observations=step)
            after = build(extended, sampling_step_observations=step)
            previous = after.scenarios.loc[after.scenarios.target_end_date <= before_data.index[-1]].reset_index(drop=True)
            pd.testing.assert_frame_equal(before.scenarios, previous)
            self.assertEqual(before.metadata['sampling_anchor'], after.metadata['sampling_anchor'])

    def test_sampling_precedes_conditioning(self):
        data = dated_frame(pd.bdate_range('2024-01-01', '2024-04-30'))
        data['DGS10'] = 4 + np.arange(len(data)) % 7 * .1
        all_sampled = build(data, horizon_months=1, sampling_step_observations=5)
        result = build(data, horizon_months=1, sampling_step_observations=5, lower_bp=-5, upper_bp=5)
        expected = all_sampled.scenarios.loc[all_sampled.scenarios.DGS10_change_bp.between(-5,5)].reset_index(drop=True)
        pd.testing.assert_frame_equal(result.scenarios, expected)
        # This fixture distinguishes endpoint sampling from sampling qualifying rows.
        qualifying = build(data, horizon_months=1, lower_bp=-5, upper_bp=5).scenarios
        wrong = qualifying.iloc[::-1].iloc[::5].iloc[::-1].reset_index(drop=True)
        self.assertNotEqual(result.scenarios.scenario_id.tolist(), wrong.scenario_id.tolist())

    def test_horizons_one_three_six_are_independent_of_step(self):
        data = scenario_frame()
        for horizon, first in ((1, '2024-02-01'), (3, '2024-04-01'), (6, '2024-07-01')):
            candidates = data.index[data.index >= pd.Timestamp(first)]
            for step in (1, 5, 20):
                with self.subTest(horizon=horizon, step=step):
                    result = build(data, horizon_months=horizon, sampling_step_observations=step)
                    self.assertEqual(result.scenarios.target_end_date.tolist(), list(candidates[::step][::-1]))
                    for row in result.scenarios.itertuples():
                        self.assertEqual(row.target_start_date, row.target_end_date - pd.DateOffset(months=horizon))

    def test_six_calendar_months_handle_month_ends_and_leap_years(self):
        for year, feb_end in ((2024, '2024-02-29'), (2025, '2025-02-28')):
            data = dated_frame(pd.date_range(f'{year}-01-01', f'{year}-12-31'))
            result = build(data)
            august = result.scenarios.loc[result.scenarios.target_end_date == pd.Timestamp(f'{year}-08-31')].iloc[0]
            self.assertEqual(august.target_start_date, pd.Timestamp(feb_end))
            self.assertEqual(august.start_date, pd.Timestamp(feb_end))
            self.assertEqual(august.end_date, pd.Timestamp(f'{year}-08-31'))
            self.assertEqual(august.elapsed_days, 184)

    def test_boundary_missing_yields_use_only_complete_inside_dates(self):
        data = scenario_frame()
        data.loc['2024-07-01', 'DGS2'] = np.nan
        data.loc['2024-12-30', 'DGS30'] = np.nan
        result = build(data)
        row = result.scenarios.iloc[0]
        self.assertEqual(row.target_start_date, pd.Timestamp('2024-06-30'))
        self.assertEqual(row.start_date, pd.Timestamp('2024-07-02'))
        self.assertEqual(row.end_date, pd.Timestamp('2024-12-31'))
        self.assertEqual(row.shortfall_days, 2)
        self.assertFalse((result.scenarios.target_end_date == pd.Timestamp('2024-12-30')).any())
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

    def test_seven_day_shortfall_accepted_eight_rejected_without_outside_search(self):
        for first_inside, expected in (('2026-05-03', 1), ('2026-05-04', 0)):
            with self.subTest(first_inside=first_inside):
                data = dated_frame(['2026-01-01', '2026-04-25', first_inside, '2026-10-26'])
                result = build(data)
                self.assertEqual(len(result.scenarios), expected)
                if expected:
                    row = result.scenarios.iloc[0]
                    self.assertEqual(row.shortfall_days, 7)
                    self.assertEqual(row.start_date, pd.Timestamp(first_inside))
                    self.assertEqual(row.target_start_date, pd.Timestamp('2026-04-26'))
                    self.assertEqual(row.end_date, pd.Timestamp('2026-10-26'))
                else:
                    self.assertEqual(result.metadata['counts']['shortfall_excluded'], 1)

    def test_every_vector_matches_independent_inside_window_enumeration(self):
        data = scenario_frame()
        for step in (1, 5, 20):
            result = build(data, condition_tenor='DGS2', lower_bp=36.4, upper_bp=36.6, sampling_step_observations=step)
            ends = data.index[data.index >= pd.Timestamp('2024-07-01')][::step][::-1]
            expected = []
            for end in ends:
                start = end - pd.DateOffset(months=6)
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

    def test_sampling_precedes_insufficient_and_shortfall_exclusions(self):
        data = dated_frame(['2025-12-01', '2026-01-01', '2026-07-05', '2026-08-01'])
        counts = build(data).metadata['counts']
        self.assertEqual(counts['candidate_endpoints'], 2)
        self.assertEqual(counts['insufficient_observations_excluded'], 1)
        self.assertEqual(counts['shortfall_excluded'], 1)
        sampled = build(data, sampling_step_observations=2).metadata['counts']
        self.assertEqual(sampled['sampled_endpoints'], 1)
        self.assertEqual(sampled['insufficient_observations_excluded'], 1)
        self.assertEqual(sampled['shortfall_excluded'], 0)
        for step in (1,5,20):
            counts = build(sampling_step_observations=step).metadata['counts']
            self.assertEqual(counts['sampled_endpoints'], counts['intended_windows'])
            self.assertEqual(counts['intended_windows'], counts['eligible_windows'] +
                             counts['insufficient_observations_excluded'] + counts['shortfall_excluded'])

    def test_reference_bounds_control_earliest_candidate_anchor(self):
        data = scenario_frame()
        data.loc['2024-01-01', 'DGS30'] = np.nan
        result = build(data, reference_start='2024-01-01', reference_end='2024-11-30', sampling_step_observations=5)
        self.assertEqual(result.metadata['reference'], dict(requested_start='2024-01-01',
                         requested_end='2024-11-30', effective_start='2024-01-02', effective_end='2024-11-29'))
        self.assertEqual(result.metadata['sampling_anchor'], '2024-07-02')
        self.assertTrue((result.scenarios.target_start_date >= pd.Timestamp('2024-01-02')).all())
        self.assertEqual(build(data).metadata['counts']['reference_rows'], len(data)-1)
        self.assertEqual(build(data).metadata['counts']['incomplete_rows_excluded'], 0)
        with self.assertRaisesRegex(ValueError, 'No complete'):
            build(data, reference_start='2025-01-01')

    def test_invalid_observation_steps_rejected_in_both_entry_points(self):
        data = scenario_frame()
        for value in (0, -1, 1.5, 1.0, True, False, np.bool_(True), None, '5', [], {}, np.nan, np.inf):
            for function in (lambda **kw: build(data, **kw),
                             lambda **kw: TreasuryMarketAnalysis(data).scenarios(condition_tenor='DGS10', lower_bp=-25, upper_bp=25, **kw)):
                with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'sampling_step_observations.*positive integer'):
                    function(sampling_step_observations=value)
        self.assertEqual(build(data, sampling_step_observations=np.int64(5)).metadata['sampling_step_observations'], 5)
        self.assertEqual(len(build(data, sampling_step_observations=10**100).scenarios), 1)

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
                        {'horizon_months':True},
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
