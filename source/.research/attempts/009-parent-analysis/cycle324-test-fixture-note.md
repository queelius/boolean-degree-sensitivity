The first cycle-324 pytest invocation failed at collection, before testing
any mathematics: `dict(known,1:2)` is invalid Python syntax. The independent
real-data audit ran separately and checked 8,512 safe-component rows plus
the literal coordinate transport. Its output remains unchanged.

`test_verify_matched_safe_count_exclusion_v2.py` corrects the dictionary
fixture to `{**known, 1: 2}` and adds the empty-family rejection control.
The original test and its failed log are retained as historical artifacts;
they are not evidence of passing tests. No production algorithm changed.
