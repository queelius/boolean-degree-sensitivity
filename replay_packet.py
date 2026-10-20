"""Replay the declared controls and ten cases inside the isolated container."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from time import monotonic
import json
import subprocess
import sys
import xml.etree.ElementTree as ET

PACKET = Path("/packet")
RESULTS = Path("/results")
plan = json.loads((PACKET / "REPLAY-PLAN.json").read_text())
workdir = Path(plan["workdir"])
started = datetime.now(timezone.utc).isoformat()
records = []


def run(name, argv, timeout):
    start = monotonic()
    with (RESULTS / f"{name}.log").open("x") as stream:
        result = subprocess.run([sys.executable, *argv], cwd=workdir,
                                stdout=stream, stderr=subprocess.STDOUT, timeout=timeout)
    record = dict(name=name, argv=[sys.executable, *argv], returncode=result.returncode,
                  seconds=monotonic() - start)
    records.append(record)
    print(json.dumps(record), flush=True)
    if result.returncode:
        raise RuntimeError(f"Replay stage failed: {name}")


def digest(path):
    value = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


# This check happens inside the container. The original research directory is
# not mounted: the identical path denotes only the staged, read-only source.
files_checked = 0
for name in plan["source_manifests"]:
    manifest = json.loads((PACKET / name).read_text())
    for item in manifest["files"]:
        original = Path(item["original_path"])
        if not original.is_relative_to(Path(plan["original_root"])):
            raise ValueError("Source outside the declared packet root")
        if digest(original) != item["sha256"]:
            raise ValueError(f"Frozen source checksum mismatch: {original}")
        files_checked += 1
run("controls", ["-m", "pytest", "-q", "-p", "no:cacheprovider",
                 *plan["tests"], "--junitxml=/results/controls.xml"], 180)
xml = ET.parse(RESULTS / "controls.xml").getroot()
cases = list(xml.iter("testcase"))
assert len(cases) == plan["expected_test_count"]
assert not any(item.tag in {"failure", "error", "skipped"} for item in xml.iter())
run("domain-deletions", ["verify_matched_whole_family.py", "--source", plan["propagation"],
                         "--output", "/results/domain-deletions.json"], 240)
deletions = json.loads((RESULTS / "domain-deletions.json").read_text())
assert deletions["status"] == "INDEPENDENTLY_VERIFIED_MATCHED_WHOLE_FAMILY_DELETIONS"
assert sum(r["verified_whole_family_deletions"] for r in deletions["records"]) == plan["expected_deletions"]
assert not any(r["conditional_case_excluded"] for r in deletions["records"])
for case in plan["cases"]:
    for stage in case["stages"]:
        name = f"first-{case['first_row']}-stage-{stage['cycle']}"
        argv = list(stage["argv"])
        output = RESULTS / f"{name}.json"
        argv[argv.index("--output") + 1] = str(output)
        run(name, argv, 240)
        result = json.loads(output.read_text())
        assert result["scope"] == stage["scope"]
        assert {k: result[k] for k in stage["expected"]} == stage["expected"]
receipt = dict(
    kind="staged_packet_independent_replay",
    started_at=started, finished_at=datetime.now(timezone.utc).isoformat(),
    source_files_hash_verified=files_checked, controls_passed=len(cases),
    domain_deletions_replayed=True, cases_replayed=len(plan["cases"]),
    source_mounted_read_only=True, original_workspace_mounted=False,
    upstream_historical_reductions_replayed=False,
    all_selected_input_and_certificate_checks_passed=True,
    global_question_status="OPEN", stages=records,
)
(RESULTS / "REPLAY-RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps({k: v for k, v in receipt.items() if k != "stages"}), flush=True)
