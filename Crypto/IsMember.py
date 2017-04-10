import unittest
import os, sys
import gmpy2
from gmpy2 import mpz
from gmpy2 import jacobi
from Crypto.SecurityParams import SecurityParams

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils           import AssertNumeric, AssertClass
from Crypto.SecurityParams import secparams_default, SecurityParams

def IsMember(x, secparams=secparams_default):
    """
    Algorithm 7.2: Checks if x is an element of G_q.
    The core of the algorithm is the computation of the Jacobi symbol for which we refer to existing algorithms

    Args:
        x (mpz):     The number to test x \in N

    Returns:
        list:        A list with length n containing the first n prime numbers in G_p
    """

    AssertNumeric(x)
    AssertClass(secparams, SecurityParams)

    if 1 <= x and x < secparams.p:
        j = jacobi(x, secparams.p)

        if j == 1:
            return True

    return False

class GetPrimesTest(unittest.TestCase):
    def testOne(self):
        # Test if the numbers 1,3,4,5,9 are recognized as members of G_q for q = 5 and p = 11
        dummySecParams = SecurityParams(4,4,
                11,
                5,
                2,4,9,787,131,6,64,131,8,True)
        self.assertTrue(IsMember(1,dummySecParams))
        self.assertFalse(IsMember(2, dummySecParams))
        self.assertTrue(IsMember(3, dummySecParams))
        self.assertTrue(IsMember(4, dummySecParams))
        self.assertTrue(IsMember(5, dummySecParams))
        self.assertFalse(IsMember(6, dummySecParams))
        self.assertFalse(IsMember(7, dummySecParams))
        self.assertFalse(IsMember(8, dummySecParams))
        self.assertTrue(IsMember(9, dummySecParams))

if __name__ == '__main__':
    unittest.main()
