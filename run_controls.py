"""Run the frozen packet's small controls from this source-only checkout."""
from pathlib import Path
import json
import subprocess
import sys

root = Path(__file__).resolve().parent
plan = json.loads((root / "REPLAY-PLAN.json").read_text())
tests = plan["tests"]
if not tests or any(Path(name).name != name for name in tests):
    raise ValueError("The control plan must name local test files.")
result = subprocess.run(
    [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *tests],
    cwd=root / "source/.research/attempts/009-parent-analysis",
)
raise SystemExit(result.returncode)
