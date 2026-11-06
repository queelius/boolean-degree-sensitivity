"""Literal serialization, source pins and bounded process I/O; no target search."""
import copy
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def pin(path):
    path = Path(path).resolve()
    sha = hashlib.sha256()
    with path.open('rb') as stream:
        for part in iter(lambda: stream.read(1 << 20), b''):
            sha.update(part)
    return dict(path=str(path), sha256=sha.hexdigest(), bytes=path.stat().st_size)


def read_pinned(ref):
    actual = pin(ref['path'])
    need(actual['sha256'] == ref['sha256'] and ('bytes' not in ref or actual['bytes'] == ref['bytes']), 'source hash/size differs')
    return json.loads(Path(ref['path']).read_text())


def write_json(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, separators=(',', ':'), sort_keys=True, allow_nan=False)
        stream.write('\n')
    return pin(path)


def unique_context(contexts, model_id):
    key = json.dumps(model_id, sort_keys=True, separators=(',', ':'), allow_nan=False)
    matches = [c for c in contexts if json.dumps(c['model_id'], sort_keys=True, separators=(',', ':'), allow_nan=False) == key]
    need(len(matches) == 1, 'missing/aliased exact native context')
    return matches[0]


def native_model(common, context, gate, gate_ref):
    need(type(common['n']) is int and type(context['n']) is int and common['n'] == context['n'], 'native dimensions differ')
    header = dict(kind='NATIVE_SIGNED_STAR_FULL_P', n=common['n'], constant=context['model_id']['constant'],
                  native_identity=copy.deepcopy(context['model_id']['native_identity']),
                  root=context['root'], source_to_physical=copy.deepcopy(context['source_to_physical']),
                  root_link=copy.deepcopy(context['root_link']), special_edges=copy.deepcopy(context['special_edges']),
                  root_nonneighbor_physical_slots=copy.deepcopy(context['root_nonneighbor_physical_slots']),
                  common_source=copy.deepcopy(gate['common_source']), context_source=copy.deepcopy(gate['context_source']),
                  row_gate=copy.deepcopy(gate_ref), row_order='common.rows followed by context.rows')
    return dict(schema_version=1, header=header, variables=common['variables'], rows=common['rows']+context['rows'])


def solution(text, variables):
    need(type(variables) is int and variables >= 0, 'exact variable dimension required')
    values, status, terminated = {}, False, False
    for line in text.splitlines():
        tokens = line.split()
        if not tokens or tokens[0] == 'c':
            continue
        if tokens[0] == 's':
            need(not status and tokens == ['s', 'SATISFIABLE'], 'not exactly one SAT model status')
            status = True
        else:
            need(tokens[0] == 'v' and status and not terminated, 'unexpected model record')
            for position, token in enumerate(tokens[1:], 1):
                value = int(token)
                if value == 0:
                    need(position == len(tokens)-1, 'model terminator is not final')
                    terminated = True
                else:
                    need(1 <= abs(value) <= variables and abs(value) not in values, 'model variable omitted/aliased/outside dimension')
                    values[abs(value)] = value > 0
    need(status and terminated and set(values) == set(range(1, variables+1)), 'incomplete literal SAT assignment')
    return values


def empty_additions(text):
    empty = []
    for line in text.splitlines():
        words = line.split()
        if not words:
            continue
        need(len(words) >= 3 and int(words[0]) > 0, 'invalid ASCII LRAT record')
        if words[1] == 'd':
            deleted = [int(x) for x in words[2:]]
            need(len(deleted) >= 2 and deleted[-1] == 0 and all(x > 0 for x in deleted[:-1]), 'invalid LRAT deletion')
            continue
        fields = [int(x) for x in words[1:]]
        need(fields.count(0) == 2 and fields[-1] == 0, 'invalid LRAT addition terminators')
        first = fields.index(0)
        if first == 0:
            empty.append(int(words[0]))
    return empty


def solver_status(result):
    if result['timed_out']:
        return 'WALL_TIMEOUT_INCONCLUSIVE'
    return {10: 'SAT_CANDIDATE', 20: 'UNSAT_PROPOSAL'}.get(result['exit_code'], 'SOLVER_EXIT_INCONCLUSIVE')


def lrat_accepted(result, stdout, empties):
    return not result['timed_out'] and result['exit_code'] == 20 and 's VERIFIED' in stdout.splitlines() and bool(empties)


def execute(argv, stem, cpu=(5, 7), wall=10):
    need(type(cpu) is tuple and len(cpu) == 2 and all(type(x) is int for x in cpu) and 0 < cpu[0] <= cpu[1] <= 20,
         'bounded exact process CPU limits required')
    need(type(wall) in (int, float) and 0 < wall <= 30, 'bounded wall limit required')
    stem = Path(stem)
    stdout, stderr = Path(str(stem)+'.stdout.log'), Path(str(stem)+'.stderr.log')
    limits = dict(CPU_soft_seconds=cpu[0], CPU_hard_seconds=cpu[1], wall_seconds=wall,
                  memory_bytes=536870912, each_output_file_bytes=67108864)
    def bound():
        resource.setrlimit(resource.RLIMIT_CPU, cpu)
        resource.setrlimit(resource.RLIMIT_AS, (limits['memory_bytes'], limits['memory_bytes']))
        resource.setrlimit(resource.RLIMIT_FSIZE, (limits['each_output_file_bytes'], limits['each_output_file_bytes']))
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    started = time.monotonic()
    with stdout.open('x') as out, stderr.open('x') as err:
        child = subprocess.Popen(list(map(str, argv)), stdout=out, stderr=err, preexec_fn=bound, start_new_session=True)
        timed_out = False
        try:
            code = child.wait(timeout=wall)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(child.pid, signal.SIGKILL)
            code = child.wait()
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    return dict(argv=list(map(str, argv)), pid=child.pid, exit_code=code, timed_out=timed_out,
                wall_seconds=time.monotonic()-started, limits=limits,
                child_CPU_seconds=after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,
                stdout=pin(stdout), stderr=pin(stderr))


def kernel_record(adapter):
    program = []
    for spec in adapter.program:
        fields = dict(kind=type(spec).__name__.upper(), literals=list(spec.literals))
        need(fields['kind'] in ('COUNT', 'CLAUSE'), 'unexpected typed kernel command')
        if fields['kind'] == 'COUNT':
            fields.update(lower=spec.lower, upper=spec.upper)
        program.append(fields)
    return dict(program=program, gates=[dict(output=g.output, kind=g.kind.name, inputs=list(g.inputs)) for g in adapter.gates])


def write_cnf(path, adapter, encoding_record):
    need(encoding_record['total_CNF_variables'] == adapter.variables and encoding_record['CNF_clauses'] == len(adapter.clauses),
         'changed audited CNF dimensions')
    digest = hashlib.sha256()
    digest.update(b'[')
    with Path(path).open('x') as stream:
        stream.write(f'p cnf {adapter.variables} {len(adapter.clauses)}\n')
        for i, row in enumerate(adapter.clauses):
            need(all(type(x) is int and 0 < abs(x) <= adapter.variables for x in row), 'invalid DIMACS literal')
            stream.write((' '.join(map(str, row))+' ' if row else '')+'0\n')
            if i:
                digest.update(b',')
            digest.update(json.dumps(row, separators=(',', ':')).encode())
    digest.update(b']')
    need(digest.hexdigest() == encoding_record['CNF_clause_digest'], 'changed audited clause stream')
    return dict(**pin(path), clause_digest=digest.hexdigest())
