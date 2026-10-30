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


def scenario_frame():
    """Synthetic irregular leap-year observations, not downloaded yields."""
    dates = ['2024-01-30', '2024-01-31', '2024-02-28', '2024-02-29',
             '2024-03-28', '2024-04-30', '2024-07-31', '2024-08-28',
             '2024-08-30', '2025-01-31']
    values = [[4, 4.5, 5], [4.1, 4.6, 5.1], [4.2, 4.7, 5], [4.3, 4.8, 4.9],
              [3.9, 4.5, 5.2], [3.8, 4.4, 5.3], [4.3, 4.35, 5.6],
              [4.4, 5.05, 5.7], [4.6, 5.3, 5.8], [4.1, 4.4, 5.9]]
    data = pd.DataFrame(values, index=pd.to_datetime(dates), columns=['DGS2','DGS10','DGS30'])
    data.index.name = 'date'
    data.attrs['metadata'] = deepcopy(example_frame().attrs['metadata'])
    for info in data.attrs['metadata'].values():
        info['source'] = 'Synthetic scenario fixture, not market data'
    return data


def build(data=None, **kwargs):
    options = dict(condition_tenor='DGS10', lower_bp=-1000, upper_bp=1000)
    options.update(kwargs)
    return build_conditional_scenarios(scenario_frame() if data is None else data, **options)


class ScenarioTests(unittest.TestCase):
    def test_default_six_months_complete_joint_vectors_and_inclusive_bounds(self):
        data = scenario_frame()
        before = data.copy(deep=True)
        result = build(data, lower_bp=-25, upper_bp=-25)
        self.assertIsInstance(result, ScenarioSet)
        row = result.scenarios.iloc[0]
        self.assertEqual(len(result.scenarios), 1)
        self.assertEqual(row.scenario_id, 'UST_20240131_20240731')
        self.assertEqual(row.start_date, pd.Timestamp('2024-01-31'))
        self.assertEqual(row.end_date, pd.Timestamp('2024-07-31'))
        self.assertEqual(row.elapsed_days, 182)
        np.testing.assert_allclose(row[list(CHANGE_COLUMNS)].astype(float), [20,-25,50])
        self.assertEqual(result.metadata['horizon_months'], 6)
        self.assertEqual(result.metadata['sampling'], 'monthly')
        self.assertEqual(result.metadata['condition'], {'tenor':'DGS10', 'lower_bp':-25., 'upper_bp':-25., 'inclusive':True})
        pd.testing.assert_frame_equal(data, before)
        self.assertTrue(build(data, lower_bp=-24.999, upper_bp=-24.999).scenarios.empty)
        self.assertIn('not independent', result.metadata['interpretation'])

    def test_monthly_daily_leap_clipping_actual_dates_and_elapsed_days(self):
        result = build(horizon_months=1)
        jan = result.scenarios.iloc[0]
        self.assertEqual(jan.start_date, pd.Timestamp('2024-01-31'))
        self.assertEqual(jan.target_end_date, pd.Timestamp('2024-02-29'))
        self.assertEqual(jan.end_date, pd.Timestamp('2024-02-29'))
        self.assertEqual(jan.elapsed_days, 29)
        feb = result.scenarios.iloc[1]
        self.assertEqual(feb.target_end_date, pd.Timestamp('2024-03-29'))
        self.assertEqual(feb.end_date, pd.Timestamp('2024-03-28'))
        daily = build(sampling='daily', horizon_months=1)
        self.assertEqual(daily.scenarios.iloc[0].start_date, pd.Timestamp('2024-01-30'))
        self.assertEqual(daily.scenarios.iloc[0].end_date, pd.Timestamp('2024-02-29'))
        self.assertEqual(daily.scenarios.iloc[0].elapsed_days, 30)
        self.assertGreater(len(daily.scenarios), len(result.scenarios))
        self.assertTrue(set(result.scenarios.scenario_id).issubset(daily.scenarios.scenario_id))

    def test_every_vector_matches_independent_endpoint_subtraction(self):
        data = scenario_frame()
        for sampling in ('daily','monthly'):
            result = build(data, condition_tenor='DGS2', lower_bp=-30, upper_bp=30,
                           horizon_months=1, sampling=sampling)
            # Independent enumeration, preserving whole vectors before conditioning.
            dates = data.index
            starts = [d for d in dates if sampling == 'daily' or
                      d == max(x for x in dates if (x.year,x.month)==(d.year,d.month))]
            expected = []
            for start in starts:
                target = start + pd.DateOffset(months=1)
                ends = [d for d in dates if d <= target and (d.year,d.month)==(target.year,target.month)]
                if target > max(dates) or not ends:
                    continue
                end = max(ends)
                change = (data.loc[end] - data.loc[start])*100
                if -30 - 1e-9 <= change.DGS2 <= 30 + 1e-9:
                    expected.append((start,end,change))
            self.assertEqual(len(result.scenarios),len(expected))
            for row, (start,end,change) in zip(result.scenarios.itertuples(), expected):
                self.assertEqual((row.start_date,row.end_date), (start,end))
                np.testing.assert_allclose([getattr(row,c) for c in CHANGE_COLUMNS],change,atol=1e-10)

    def test_missing_dates_never_fill_and_missing_target_month_skips(self):
        data = scenario_frame()
        data.loc['2024-02-29','DGS30'] = np.nan
        result = build(data, horizon_months=1)
        self.assertEqual(result.scenarios.iloc[0].end_date,pd.Timestamp('2024-02-28'))
        self.assertFalse((result.scenarios.start_date == pd.Timestamp('2024-02-29')).any())
        self.assertEqual(result.metadata['counts']['incomplete_rows_excluded'],1)
        data.loc['2024-02-28','DGS2'] = np.nan
        result = build(data, horizon_months=1)
        self.assertFalse((result.scenarios.start_date == pd.Timestamp('2024-01-31')).any())
        self.assertGreater(result.metadata['counts']['unmatched_target_months_excluded'],0)
        self.assertFalse(result.scenarios[list(CHANGE_COLUMNS)].isna().any().any())
        counts=result.metadata['counts']
        self.assertEqual(counts['sampled_starts'], counts['eligible_windows'] + counts['immature_targets_excluded'] + counts['unmatched_target_months_excluded'])

    def test_reference_bounds_complete_coverage_and_no_immature_windows(self):
        data = scenario_frame()
        data.loc['2024-01-30','DGS30'] = np.nan
        result=build(data, horizon_months=1, reference_start='2024-01-01',reference_end='2024-08-29')
        self.assertEqual(result.metadata['reference'],dict(requested_start='2024-01-01',requested_end='2024-08-29',effective_start='2024-01-31',effective_end='2024-08-28'))
        self.assertTrue((result.scenarios.target_end_date <= pd.Timestamp('2024-08-28')).all())
        self.assertGreater(result.metadata['counts']['immature_targets_excluded'],0)
        self.assertEqual(build(data).metadata['reference']['effective_start'],'2024-01-31')
        self.assertEqual(build(data).metadata['reference']['effective_end'],'2025-01-31')
        self.assertEqual(build(data).metadata['counts']['reference_rows'], len(data)-1)
        self.assertEqual(build(data).metadata['counts']['incomplete_rows_excluded'], 0)

    def test_ids_reproducible_across_bounds_order_and_source_mutation(self):
        data=scenario_frame()
        result=build(data)
        reverse=build(data.iloc[::-1])
        pd.testing.assert_frame_equal(result.scenarios,reverse.scenarios)
        selected=build(data,lower_bp=-25,upper_bp=-25)
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
            self.assertEqual(list(result.scenarios.columns), ['scenario_id','start_date','target_end_date','end_date','elapsed_days',*CHANGE_COLUMNS])
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
        singleton=build(lower_bp=-25,upper_bp=-25)
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
