import unittest
import gmpy2
from gmpy2 import mpz
from SecurityParams import secparams_def, secparams_l0
from Utils import isNummericType, ToByteArray

def RecHash(v, secparams=secparams_def):        
    """
    Algorithm 4.9: Computes the hash value h(v_1,...v_k) of multiple inputs v_1..v_k in a recursive manner.

    @type   v:  list
    @param  v:  Input values v_i \in  V_i, V_i unspecified, k >= 0

    @rtype:     bytes
    @return:    An immutable array of bytes representing the recursive hash of the input values with a length corresponding to the used hash function
    """     
    # check if v is a list
    isSingleElementOfList = False
    if isinstance(v,list) and len(v) == 1:
            isSingleElementOfList = True
    
    if not isinstance(v, list) and not isinstance(v, tuple) or isSingleElementOfList:   # single objects (int, string, bytearray, ...)
        v0 = v[0] if isSingleElementOfList else v
        
        if isinstance(v0, bytearray) or v0.__class__.__name__ == 'bytes':
            return secparams.hash(v0)
        if isinstance(v0, int) or v0.__class__.__name__ == 'mpz':
           return secparams.hash(ToByteArray(v0))
        if isinstance(v0, str):
            return secparams.hash(v0.encode('utf-8'))
        if isinstance(v0, list):
            return RecHash(v0, secparams)

        return bytes()
    else:                               # if v is a list or a tuple
        res = bytearray()
        for vi in v:
            # performance optimization: Iteration instead of recursion 
            # res +=  RecHash(vi, secparams)    # concatenate hashes           
            if isinstance(vi, bytearray) or vi.__class__.__name__ == 'bytes':
                res += secparams.hash(vi)
            if isinstance(vi, int) or vi.__class__.__name__ == 'mpz':
               res += secparams.hash(ToByteArray(vi))
            if isinstance(vi, str):
                res += secparams.hash(vi.encode('utf-8'))
            if isinstance(vi, list):
                res += RecHash(vi, secparams)

        return secparams.hash(res)            # hash the concatenation of the hashes

# Unit Tests
class RecHashTest(unittest.TestCase):
    def testOne(self):
        self.assertTrue(RecHash(123) == RecHash(123))     # test for deterministic output
        self.assertTrue(RecHash(123) == RecHash([123]))   # test if we avoid h(h(B1)) for a single input
        self.assertTrue(RecHash(123) == RecHash([[123]]))
        self.assertTrue(len(RecHash(mpz(1234))) > 0)
        self.assertTrue(len(RecHash([mpz(1234),mpz(2304)])) > 0)     

if __name__ == '__main__':
    unittest.main()