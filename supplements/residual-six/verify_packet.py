"""Relative standard-library replay. No owning-workspace or network access."""
from hashlib import sha256
from pathlib import Path, PurePosixPath
from datetime import date
from urllib.parse import urlparse
import argparse
import ast
import json
import time

import controls
from kernels import endpoint, core, disk


def require(condition, message):
    if not condition:
        raise ValueError(message)


def files_under(root):
    root = Path(root)
    return sorted(p.relative_to(root).as_posix() for p in root.rglob('*')
                  if p.is_file() and '__pycache__' not in p.parts
                  and p.suffix != '.pyc' and p.relative_to(root).as_posix() != 'SOURCE-MANIFEST.json')


def safe_file(root, name):
    require(type(name) is str, 'path must be a string')
    relative = PurePosixPath(name)
    require(name == relative.as_posix() and not relative.is_absolute()
            and name not in ('', '.') and '..' not in relative.parts,
            'noncanonical or escaping relative path')
    root = Path(root).resolve()
    path = root.joinpath(*relative.parts)
    require(path.is_file() and not path.is_symlink(), 'missing or aliased file')
    require(path.resolve().is_relative_to(root), 'path escapes packet')
    return path


def make_manifest(root, paths):
    result = []
    for name in sorted(paths):
        body = safe_file(root, name).read_bytes()
        result.append({'path': name, 'bytes': len(body), 'sha256': sha256(body).hexdigest()})
    return {'schema_version': 1, 'algorithm': 'sha256', 'files': result}


def check_manifest(root, manifest):
    require(manifest.get('schema_version') == 1 and manifest.get('algorithm') == 'sha256',
            'unsupported manifest schema')
    rows = manifest['files']
    names = [row['path'] for row in rows]
    require(len(names) == len(set(names)), 'duplicate manifest row')
    require(names == sorted(names) and names == files_under(root),
            'manifest omits, aliases, reorders or invents packet files')
    for row in rows:
        require(type(row['bytes']) is int and row['bytes'] >= 0, 'invalid byte count')
        body = safe_file(root, row['path']).read_bytes()
        require(len(body) == row['bytes'] and sha256(body).hexdigest() == row['sha256'],
                'packet bytes differ: ' + row['path'])
    return len(rows)


def check_claims(document):
    require(document.get('schema_version') == 2, 'unsupported mathematical claims schema')
    require(document.get('global_goal_complete') is False, 'invalid global promotion')
    require(not {'new_version_doi', 'publication_status', 'proposed_version'} & set(document),
            'archival state belongs in publication metadata, not mathematical claims')
    assumptions = document['assumptions']
    require(all(a['bundled_proof_complete'] is False for a in assumptions),
            'unbundled premise promoted to a complete proof')
    claims = document['claims']
    nodes = {x['id']: x for x in assumptions + claims}
    require(len(nodes) == len(assumptions) + len(claims), 'duplicate claim or premise')
    inherited = {a['id'] for a in assumptions}
    completed = set(inherited)
    conditional = {key: True for key in inherited}
    for claim in claims:
        dependencies = claim['depends_on']
        require(len(dependencies) == len(set(dependencies))
                and set(dependencies) <= completed, 'invalid or cyclic claim dependency')
        require(claim['written_proof_bundled'] is True, 'missing new written proof')
        depends_on_external = any(conditional[key] for key in dependencies)
        require(claim['conditional_on_inherited_theorems'] is depends_on_external,
                'inherited conditionality changed')
        require(claim['full_dependency_closure_bundled'] is (not depends_on_external),
                'unbundled dependency closure promoted')
        conditional[claim['id']] = depends_on_external
        completed.add(claim['id'])
    require(nodes['OLD_LOCAL_012']['constants'] == [1, 2]
            and nodes['BASELINE_LE3']['constant_upper_bound'] == 3,
            'old constant guard changed')
    require(nodes['APPLICATION']['full_Boolean_application_self_contained'] is False,
            'whole Boolean application promoted')
    require(nodes['UNION12']['negative_union_lower_bound'] == 12,
            'support conclusion changed')


def https_url(value):
    require(type(value) is str, 'URL must be a string')
    parsed = urlparse(value)
    require(parsed.scheme == 'https' and bool(parsed.netloc), 'HTTPS evidence URL required')


def check_publication(plan, citation):
    """Check lifecycle consistency; this does not prove any external event."""
    require(plan['schema_version'] == 2 and plan['state'] in
            ('LOCAL_STAGING', 'DOI_RESERVED', 'PUBLISHED'), 'unsupported publication state')
    prepared, observed = date.fromisoformat(plan['prepared_on']), date.fromisoformat(plan['as_of'])
    require(prepared <= observed, 'preparation after observation')
    require(citation['version'] == plan['version'] and citation['title'] == plan['title'],
            'citation/version metadata differs')
    archive, source = plan['archive'], plan['source_disclosure']
    def event_date(value, evidence):
        require(value is not None and evidence is not None, 'date lacks observed event/evidence')
        parsed = date.fromisoformat(value)
        require(prepared <= parsed <= observed, 'invented, backdated or future new-event date')
        https_url(evidence)
        return parsed
    if any(value is not None for value in source.values()):
        require(all(value is not None for value in source.values()), 'partial source event')
        require(type(source['commit']) is str and len(source['commit']) == 40
                and set(source['commit']) <= set('0123456789abcdef'), 'exact source commit required')
        https_url(source['url']); event_date(source['observed_on'], source['evidence'])
    if plan['state'] == 'LOCAL_STAGING':
        require(all(value is None for value in archive.values()) and 'doi' not in citation,
                'staging metadata invents an archival event')
    else:
        doi = archive['doi']
        require(type(doi) is str and doi.startswith('10.') and '/' in doi
                and doi not in (plan['concept_doi'], plan['predecessor_version_doi']),
                'concept/predecessor is not this new archive version')
        require(citation.get('doi') == doi, 'assigned DOI/citation mismatch')
        reserved = event_date(archive['reserved_on'], archive['reservation_evidence'])
        if plan['state'] == 'DOI_RESERVED':
            require(archive['published_on'] is None and archive['publication_evidence'] is None,
                    'reservation promoted to publication')
        else:
            published = event_date(archive['published_on'], archive['publication_evidence'])
            require(reserved <= published and source['observed_on'] is not None,
                    'publication lacks reservation/source event')


def definition_signatures(source, excluded):
    tree = ast.parse(source)
    return {node.name: ast.dump(node, include_attributes=False) for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name not in excluded}


def check_kernel_sources(root):
    provenance = json.loads(safe_file(root, 'PROVENANCE.json').read_text())
    definitions = 0
    for row in provenance['kernel_sources']:
        original = safe_file(root, row['original_path']).read_bytes()
        require(sha256(original).hexdigest() == row['original_sha256'], 'original kernel pin differs')
        body = safe_file(root, row['kernel_path']).read_text()
        retained = definition_signatures(body, [])
        expected = definition_signatures(original.decode(), row['excluded_definitions'])
        require(retained == expected and set(retained) == set(row['retained_definitions']),
                'retained mathematical definition AST differs')
        definitions += len(retained)
    return {'sources': len(provenance['kernel_sources']), 'definitions': definitions}


def canonical(value):
    return json.loads(json.dumps(value, sort_keys=True))


def new_mathematical_controls():
    core_result = core.run()
    core_result.pop('cpu_seconds')  # Only this operational timing is omitted.
    # Retain the original disk wrapper's scope flags, including its historical
    # proposed-control tag. This tag is not current claim/publication status.
    disk_result = {'status': 'PROPOSED_ELEMENTARY_DISK_I_GE3_WITH_SMALL_CONTROLS',
                   'ears': disk.ear_controls(), 'valid_countercontrols': disk.control_disks(),
                   'degree_counts': disk.allocation_controls(),
                   'valid_all_guard_disk_constructed': False, 'target_sphere_catalog_filters': 0,
                   'target_feasibility_queries': 0, 'new_solver_runs': 0, 'canonical_updates': 0,
                   'whole_pattern_exclusions': 0, 'global_goal_complete': False,
                   'global_three_disk_application_not_a_premise': True}
    return canonical({'endpoint': endpoint.run_controls(), 'core': core_result,
                      'disk': disk_result})


def check_new_expected(actual, expected):
    require(actual == expected, 'complete new mathematical payload differs')


def check_expected_incidence(actual, expected):
    require(actual == expected, 'complete incidence/allocation records differ')


def replay(root):
    start = time.process_time()
    root = Path(root)
    checked = check_manifest(root, json.loads((root / 'SOURCE-MANIFEST.json').read_text()))
    registry = json.loads((root / 'CLAIMS.json').read_text())
    check_claims(registry)
    for claim in registry['claims']:
        safe_file(root, claim['proof_path'])
    check_publication(json.loads((root / 'PUBLICATION-PLAN.json').read_text()),
                      json.loads((root / 'CITATION.cff').read_text()))
    definitions = check_kernel_sources(root)
    expected = json.loads((root / 'data/expected-controls.json').read_text())
    actual = controls.run_controls()
    actual.pop('cpu_seconds')
    require(actual == expected, 'exact portable control records differ')
    check_expected_incidence(actual['incidence'], expected['incidence'])
    check_new_expected(new_mathematical_controls(),
                       json.loads((root / 'data/expected-new-controls.json').read_text()))
    return {'schema_version': 2, 'status': 'PORTABLE_RESIDUAL6_UNION_BOUNDS_CONDITIONAL_PROOFS_AND_CONTROLS_PASS',
            'files_checked': checked, 'allocations': actual['incidence']['allocations'],
            'incidence_cases': actual['incidence']['incidence_cases'],
            'new_kernel_source_AST_checks': definitions,
            'endpoint_heptagon_triangulations': 42, 'rooted_polygon_ear_checks': 414,
            'common_core_Boolean_words': 256, 'four_offcycle_word_combinations': 1296,
            'conditional_negative_union_bound': 12,
            'inherited_local_theorems_replayed': False,
            'old_graph_classifications_replayed': False,
            'full_Boolean_application_self_contained': False,
            'publication_state_not_proved_by_math_replay': True, 'global_goal_complete': False,
            'cpu_seconds': time.process_time() - start}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    arguments = parser.parse_args(argv)
    root = Path(__file__).resolve().parent
    # Keep the packet immutable and put new receipts outside it.
    require(not arguments.output.resolve().is_relative_to(root),
            'put fresh replay output outside the frozen packet')
    result = replay(root)
    with arguments.output.open('x') as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
