import unittest
import gmpy2
from gmpy2 import mpz
from SecurityContext import SECURITYCONTEXT_DEFAULT, SECURITYCONTEXT_L0
from IsMember import IsMember

import Utils

def RecHash(v, ctx = SECURITYCONTEXT_DEFAULT):
    """
    Algorithm 4.9: Computes the hash value h(v_1,...v_k) of multiple inputs v_1..v_k in a recursive manner.

    @type   v:  list
    @param  v:  Input values v_i \in  V_i, V_i unspecified, k >= 0

    @rtype:     string
    @return:    Hash of the input
    """    

    if(type(v) is not list):             # single objects (int, string, bytearray, 

        if(type(v) is bytearray):
            return ctx.hash(v0)
        if(type(v) is int):
           return ctx.hash(Utils.ToByteArray(v))
        # if(type(v) is list): seems unnecessary

        return []
    else:                               # if v is a list with [1, ..., k] elements
        res = bytearray()
        for vi in v:
            res += RecHash(vi, ctx)     # concatenate hashes
        return ctx.hash(res)            # hash the concatenation of the hashes
   

    
# Unit Tests
class RecHashTest(unittest.TestCase):

    def testOne(self):
        v = [1, 2, 3]
        print(RecHash(v))
        

def main():
    unittest.main()   

if __name__ == '__main__':
    main()
