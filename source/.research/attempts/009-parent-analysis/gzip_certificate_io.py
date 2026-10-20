"""Atomic immutable JSON certificates with deterministic gzip compression."""
from pathlib import Path
import gzip
import json


def write_certificate(path,value):
    path=Path(path);assert not path.exists()
    encoded=json.dumps(value,ensure_ascii=False,separators=(',',':')).encode('utf-8')
    payload=gzip.compress(encoded,compresslevel=6,mtime=0)
    temporary=path.with_name(path.name+'.partial')
    with temporary.open('xb') as stream:stream.write(payload)
    temporary.replace(path)


def read_certificate(bindings,reference):
    bound=bindings.bind(reference['path'],reference['sha256'])
    value=json.loads(gzip.decompress(Path(bound['path']).read_bytes()).decode('utf-8'))
    bindings.walk(value)
    return value
