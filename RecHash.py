import gmpy2
from gmpy2 import mpz
from SecurityContext import SECURITYCONTEXT_DEFAULT
from IsMember import IsMember
from gmpy2 import byte, log2, floor
import utils

def RecHash(v, ctx = SECURITYCONTEXT_DEFAULT):
    """
    Algorithm 4.9: Computes the hash value h(v_1,...v_k) of multiple inputs v_1..v_k in a recursive manner.

    @type   v:  array
    @param  v:  Input values v_i \in  V_i, V_i unspecified, k >= 0

    @rtype:     string
    @return:    Hash of the input
    """    

    if(len(v) == 1):
        v0 = v[0]
        if(type(v0) is bytearray):
            return ctx.hash(v0)
        if(type(v0) is int):
           return ctx.hash(utils.ToByteArray(v0))
           return
    else:
        for vi in v:
            return
   