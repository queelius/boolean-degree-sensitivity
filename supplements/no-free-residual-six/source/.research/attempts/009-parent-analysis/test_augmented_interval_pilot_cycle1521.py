import copy
import unittest
from types import SimpleNamespace

import context_first_rows_cycle1438 as old_adapter
import gap_transcript_reader_cycle1436 as reader
from run_context_first_controls_cycle1438 import load_generator
import augmented_interval_pilot_cycle1521 as pilot


def row(i,terms,lower,upper):
    return dict(key=dict(family='TINY',subject=i,detail=0),terms=terms,lower=lower,upper=upper)


class AugmentedPilotTests(unittest.TestCase):
    def replay(self,rows,common,context,known=None):
        order,inverse=pilot.priority_order(common,context,len(rows)-common-context)
        model=dict(schema_version=1,header=dict(kind='TINY_AUGMENTED_NATIVE_CONTROL'),
                   variables=sorted({m for r in rows for m,a in r['terms']}),rows=rows)
        native=[SimpleNamespace(terms=tuple(map(tuple,r['terms'])),lower=r['lower'],upper=r['upper']) for r in rows]
        raw=load_generator().propagate([native[i] for i in order])
        translated=old_adapter.translate(raw,order)
        binding=reader.binding(model)
        result=reader.verify(model,dict(schema_version=1,model_binding=binding,certificate=translated),binding)
        if known is not None:self.assertTrue(reader.check_assignment(model,known))
        return order,inverse,model,raw,translated,result

    def test_noninvolutive_three_block_contradiction(self):
        rows=[row(0,[[1,-1],[2,1]],0,0),row(1,[[2,-1],[3,1]],0,0),
              row(2,[[3,1]],0,0),row(3,[[1,1]],1,1),row(4,[[2,1]],0,1),
              row(5,[[1,1]],1,1)]
        order,inverse,model,raw,translated,result=self.replay(rows,3,2)
        self.assertEqual(order,[5,3,4,0,1,2]);self.assertNotEqual(order,inverse)
        self.assertEqual(result['status'],'EXACT_CONTRADICTION_ACCEPTED')
        wrong=old_adapter.translate(raw,inverse)
        with self.assertRaises(ValueError):reader.verify(model,dict(schema_version=1,
            model_binding=reader.binding(model),certificate=wrong),reader.binding(model))

    def test_gap_two_x_equals_one(self):
        result=self.replay([row(0,[[1,2]],1,1)],0,0)[-1]
        self.assertEqual(result['status'],'EXACT_CONTRADICTION_ACCEPTED')
        self.assertEqual(result['fixed_variables'],1)

    def test_positive_conditional_incidence_and_degree_row(self):
        rows=[row(0,[[1,-4],[2,1],[3,1],[4,1],[5,1]],0,0),
              row(1,[[1,1]],1,1),row(2,[[2,1],[3,1],[4,1],[5,1]],4,4)]
        result=self.replay(rows,1,1,{i:1 for i in range(1,6)})[-1]
        self.assertEqual(result['status'],'VALID_PREFIX_INCONCLUSIVE')
        self.assertEqual(result['fixed_variables'],5)

    def test_empty_added_and_typed_counts(self):
        self.assertEqual(pilot.priority_order(2,1,0)[0],[2,0,1])
        for counts in [(True,1,1),(1,-1,1),(0,0,0),(1,1,False)]:
            with self.assertRaises(ValueError):pilot.priority_order(*counts)

    def test_setup_budget_is_not_generation_budget(self):
        self.assertEqual(pilot.cpu_plan(2.9),dict(setup_stop_CPU_seconds=4,
            generation_CPU_budget_seconds=10,total_CPU_soft_seconds=14,total_CPU_hard_seconds=15))
        for value in [True,-1,float('inf'),4.01]:
            with self.assertRaises(ValueError):pilot.cpu_plan(value)

    def test_fresh_context_selection_rejects_alias_and_closed(self):
        wanted=dict(native_identity=dict(catalog_sha256='a'*64,order=8,original_index=3),constant=1)
        context=dict(model_id=wanted,skip_future_queries=False,genuine_context_status='OPEN')
        self.assertIs(pilot.select_open([context],wanted),context)
        for records in [[],[context,context],[dict(context,skip_future_queries=True)],
                        [dict(context,model_id=dict(wanted,constant=True))]]:
            with self.assertRaises(ValueError):pilot.select_open(records,wanted)


if __name__=='__main__':unittest.main()
