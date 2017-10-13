import os
import sys
import unittest
from gmpy2 import jacobi

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils           import AssertNumeric, AssertClass
from chvote.Common.SecurityParams import SecurityParams

def IsMember(x, secparams):
    """
    Algorithm 7.2: Checks if x is an element of G_q.
    The core of the algorithm is the computation of the Jacobi symbol for which we refer to existing algorithms

    Args:
       x (mpz):                             The number to test x \in N
       secparams (SecurityParams):          Collection of public security parameters

    Returns:
       bool:                                True if x is a member of G_q, False if not
    """

    AssertNumeric(x)
    AssertClass(secparams, SecurityParams)

    if 1 <= x and x < secparams.p:
        return jacobi(x, secparams.p) == 1

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
