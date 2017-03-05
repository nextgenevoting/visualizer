import unittest
import gmpy2
from gmpy2 import mpz
from SecurityContext import SECURITYCONTEXT_DEFAULT, SECURITYCONTEXT_L0
from Utils import isNummericType, ToByteArray

def RecHash(v, ctx=SECURITYCONTEXT_DEFAULT):        
    """
    Algorithm 4.9: Computes the hash value h(v_1,...v_k) of multiple inputs v_1..v_k in a recursive manner.

    @type   v:  list
    @param  v:  Input values v_i \in  V_i, V_i unspecified, k >= 0

    @rtype:     bytes
    @return:    An immutable array of bytes representing the recursive hash of the input values with a length corresponding to the used hash function
    """   
    # check if v is a list
    typev = type(v)    

    isSingleElementOfList = False
    if typev is list and len(v) == 1:
            isSingleElementOfList = True
    
    if typev is not list and typev is not tuple or isSingleElementOfList:   # single objects (int, string, bytearray, ...)
        v0 = v[0] if isSingleElementOfList else v

        typev0 = type(v0)
        if typev0 is bytearray or v0.__class__.__name__ == 'bytes':
            return ctx.hash(v0)
        if typev0 is int or v0.__class__.__name__ == 'mpz':
           return ctx.hash(ToByteArray(v0))
        if typev0 is str:
            return ctx.hash(v0.encode('utf-8'))
        if typev0 is list:
            return RecHash(v0, ctx)

        return bytes()
    else:                               # if v is a list or a tuple
        res = bytearray()
        for vi in v:
            res +=  RecHash(vi, ctx)    # concatenate hashes
        return ctx.hash(res)            # hash the concatenation of the hashes

# Unit Tests
class RecHashTest(unittest.TestCase):
    def testOne(self):
        self.assertTrue(RecHash(123) == RecHash([123]))     # test if we avoid h(h(B1)) for a single input
        self.assertTrue(RecHash(123) == RecHash([[123]]))
        self.assertTrue(len(RecHash(mpz(1234))) > 0)
        self.assertTrue(len(RecHash([mpz(1234),mpz(2304)])) > 0)     

if __name__ == '__main__':
    unittest.main()