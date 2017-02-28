import unittest
import gmpy2
from gmpy2 import mpz
from SecurityContext import SECURITYCONTEXT_DEFAULT, SECURITYCONTEXT_L0
from IsMember import IsMember
import Utils

def RecHash(v, ctx=SECURITYCONTEXT_DEFAULT):
    """
    Algorithm 4.9: Computes the hash value h(v_1,...v_k) of multiple inputs v_1..v_k in a recursive manner.

    @type   v:  list
    @param  v:  Input values v_i \in  V_i, V_i unspecified, k >= 0

    @rtype:     string
    @return:    Hash of the input
    """

    # check if v is a list
    isSingleElementOfList = False

    if type(v) is list and len(v) == 1:
            isSingleElementOfList = True

    if type(v) is not list or isSingleElementOfList:   # single objects (int, string, bytearray,
        v0 = v

        if isSingleElementOfList:
            v0 = v[0]

        if type(v0) is bytearray:
            return ctx.hash(v0)
        if type(v0) is int:
           return ctx.hash(Utils.ToByteArray(v0))
        if type(v0) is str:
            return ctx.hash(v0.encode('utf-8'))
        if type(v0) is list:
            return RecHash(v0, ctx)

        return bytearray()
    else:                               # if v is a list with [1, ..., k] elements
        res = bytearray()
        for vi in v:
            res += RecHash(vi, ctx)     # concatenate hashes
        return ctx.hash(res)            # hash the concatenation of the hashes

# Unit Tests
class RecHashTest(unittest.TestCase):
    def testOne(self):
        self.assertTrue(RecHash(123) == RecHash([123]))     # test if we avoid h(h(B1)) for a single input
        self.assertTrue(RecHash(123) == RecHash([[123]]))

if __name__ == '__main__':
    unittest.main()
