"""Cached exact coordinate permutations of finite binary inputs."""
from functools import lru_cache
import numpy as np


@lru_cache(maxsize=2048)
def _image(image):
    n=len(image);assert n<=16 and all(type(v) is int for v in image) and sorted(image)==list(range(n))
    points=np.arange(1<<n,dtype=np.uint32);result=np.zeros(len(points),dtype=np.uint32)
    for old,new in enumerate(image):result |= ((points>>old)&1)<<new
    return tuple(map(int,result))


def input_image(image):
    assert all(type(v) is int for v in image)
    return _image(tuple(image))
