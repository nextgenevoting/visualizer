import os
import sys
import unittest

#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gmpy2 import mpz
from chvote.Utils.Utils           import AssertInt, AssertClass
from chvote.Utils.ToInteger       import ToInteger
from chvote.Utils.RecHash         import RecHash
from chvote.Common.SecurityParams import SecurityParams, secparams_l3

def GetGenerators(n, secparams):
    """
    Algorithm 7.3: Computes n independent generators of G_q. The algorithm is an adaption of the NIST standard FIPS PUB 186-4 [1, Appendix A.2.3].
    The string "chVote" guarantees that the resulting values are specific for chVote. In a more efficient implementation of this algorithm, the list of resulting generators is accumulated in a cache
    or precomputed for the largest expected value n_max >= n.

    Args:
       n (int):                             The number of primes to be calculated
       secparams (SecurityParams):          Collection of public security parameters

    Returns:
       list of mpz:                         a list with independent generators of G_p (mpz)
    """

    AssertInt(n)
    AssertClass(secparams, SecurityParams)
    assert n >= 0, "n must be greater than or equal 0"

    generators = []

    for i in range(n):
        x = 0

        while True:
            x += 1
            h = mpz(ToInteger(RecHash(["chVote", "ggen", i, x], secparams)) % secparams.p)
            h = (h ** 2) % secparams.p

            if h not in (0, 1):
                break

        generators.append(h)

    return generators

class GetGeneratorsTest(unittest.TestCase):
    def testGetGenerators(self):
        # Test if the lenght of the returned list matches the parameter n
        for i in range(20):
            self.assertTrue(len(GetGenerators(i, secparams_l3)) == i)

        # Check if all elements in the list are unique
        x = GetGenerators(50, secparams_l3)
        self.assertFalse(len(x) > len(set(x)))

if __name__ == '__main__':
    unittest.main()
