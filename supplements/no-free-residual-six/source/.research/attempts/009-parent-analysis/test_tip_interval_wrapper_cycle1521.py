import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

import run_tip_interval_pilot_cycle1521 as wrapper


class WrapperControls(unittest.TestCase):
    def test_actual_receipt_and_changed_context_or_limits(self):
        auth=json.loads((Path(__file__).parent/'tip-interval-parent-authorization-cycle1520.json').read_text())
        plan={k:copy.deepcopy(auth[k]) for k in ['model_id','sources','limits','output_prefix']}
        wrapper.check_authorization(auth,plan)
        for key,value in [('one_query',True),('no_retries',False),('genuine_projection_only',False)]:
            bad=copy.deepcopy(auth);bad[key]=value
            with self.assertRaises(ValueError):wrapper.check_authorization(bad,plan)
        for field in ['model_id','limits','sources']:
            bad=copy.deepcopy(plan)
            if field=='model_id':bad[field]['constant']=2
            elif field=='limits':bad[field]['generation_CPU_budget_seconds']=11
            else:bad[field]['inventory']['sha256']='0'*64
            with self.assertRaises(ValueError):wrapper.check_authorization(auth,bad)

    def test_pre_io_optimized_guards(self):
        for flag in ['-O','-OO']:
            run=subprocess.run([sys.executable,flag,wrapper.__file__,'--plan','/nonexistent/1521'],capture_output=True,text=True)
            self.assertNotEqual(run.returncode,0)
            self.assertIn('normal Python required before I/O',run.stderr)
            self.assertNotIn('No such file',run.stderr)


if __name__=='__main__':unittest.main()
