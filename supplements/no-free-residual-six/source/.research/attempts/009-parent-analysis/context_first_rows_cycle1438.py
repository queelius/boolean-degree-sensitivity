"""Fixed row scheduling and literal native-row translation; no inference engine."""
import copy


def need(ok,message):
    if not ok:raise ValueError(message)


def inverse_permutation(order):
    need(type(order) is list and len(order)>0 and all(type(i) is int for i in order),'typed nonempty permutation required')
    need(set(order)==set(range(len(order))),'missing or aliased row position')
    inverse=[None]*len(order)
    for generator_row,native_row in enumerate(order):inverse[native_row]=generator_row
    return inverse


def context_first(common_count,context_count):
    need(type(common_count) is int and type(context_count) is int and min(common_count,context_count)>=0 and common_count+context_count>0,'typed nonempty row counts required')
    order=list(range(common_count,common_count+context_count))+list(range(common_count))
    return order,inverse_permutation(order)


def translate(certificate,generator_to_native):
    inverse_permutation(generator_to_native)
    need(type(certificate) is dict,'literal certificate required')
    status=certificate.get('status')
    need(status in ('EXACT_INTERVAL_CONTRADICTION','INTERVAL_FIXED_POINT_INCONCLUSIVE'),'incomplete outcome cannot be translated')
    fields={'status','steps','evaluations','fixed_variables'}
    if status=='EXACT_INTERVAL_CONTRADICTION':fields|={'contradiction_row','contradiction_interval'}
    need(set(certificate)==fields,'certificate fields differ')
    need(type(certificate['steps']) is list and type(certificate['evaluations']) is int and certificate['evaluations']>=0 and type(certificate['fixed_variables']) is int and certificate['fixed_variables']>=0,'typed trace metadata required')
    result=copy.deepcopy(certificate)
    def native(index):
        need(type(index) is int and 0<=index<len(generator_to_native),'generator row alias or invalid index')
        return generator_to_native[index]
    for step in result['steps']:
        need(type(step) is dict and set(step)=={'variable','value','row'},'step fields differ')
        step['row']=native(step['row'])
    if status=='EXACT_INTERVAL_CONTRADICTION':result['contradiction_row']=native(result['contradiction_row'])
    return result
