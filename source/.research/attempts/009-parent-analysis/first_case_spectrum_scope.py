"""Structured scope for necessary models covering one complete first case."""
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CaseScope:
    geometry_index: int
    first_row: int
    quotient_path: str
    quotient_sha256: str

    def __post_init__(self):
        if any(type(i) is not int or i < 0 for i in (self.geometry_index,self.first_row)):
            raise ValueError('Require nonnegative integer case indices.')
        if not isinstance(self.quotient_path,str) or not Path(self.quotient_path).is_absolute():
            raise ValueError('Require an absolute quotient authority path.')
        if not isinstance(self.quotient_sha256,str) or len(self.quotient_sha256)!=64 or not set(self.quotient_sha256)<=set('0123456789abcdef'):
            raise ValueError('Require the exact SHA256 of the quotient authority.')

    def to_data(self):
        return dict(kind='complete_first_case',geometry_index=self.geometry_index,first_row=self.first_row,
                    quotient_authority=dict(path=self.quotient_path,sha256=self.quotient_sha256))

    @classmethod
    def from_data(cls,data):
        if not isinstance(data,dict) or set(data)!={'kind','geometry_index','first_row','quotient_authority'} or data['kind']!='complete_first_case':
            raise ValueError('Only an explicit complete first-case scope is accepted.')
        ref=data['quotient_authority']
        if not isinstance(ref,dict) or set(ref)!={'path','sha256'}:
            raise ValueError('Require a structured quotient authority reference.')
        return cls(data['geometry_index'],data['first_row'],ref['path'],ref['sha256'])


def input_scope(authority):
    if authority.get('status')!='INDEPENDENTLY_VERIFIED_FIRST_CASE_FULL_SPECTRUM_INPUTS':
        raise ValueError('Require independently verified first-case inputs.')
    for key in ('complete_original_pattern_cover','complete_word_pool_cover','complete_projected_coefficient_cover'):
        if authority.get(key) is not True:
            raise ValueError('Missing independently verified complete cover: '+key)
    if authority.get('empty_points')!=[]:
        raise ValueError('An LP requires nonempty word domains at every point.')
    return CaseScope.from_data(authority.get('scope'))
