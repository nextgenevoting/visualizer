import unittest
import os, sys
import gmpy2
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils            import AssertInt
from Utils.ToInteger        import ToInteger
from Utils.RecHash          import RecHash
from Crypto.SecurityParams  import secparams_default, secparams_l0

def GetGenerators(n, secparams=secparams_default):
    """
    Algorithm 7.3: Computes n independent generators of G_q. The algorithm is an adaption of the NIST standard FIPS PUB 186-4 [1, Appendix A.2.3].
    The string "chVote" guarantees that the resulting values are specific for chVote.

    Args:
       n (int):     The number of primes to be calculated

    Returns:
       list:        a list with independent generators of G_p
    """
    AssertInt(n)

    generators = []

    for i in range(0, n):
        x = 0

        while True:
            x += 1
            h = mpz(ToInteger(RecHash(["chVote", i, x])) % secparams.p)
            h = (h ** 2) % secparams.p

            if h not in (0, 1, secparams.h, secparams.g) and h not in generators:
                break

        generators.append(h)

    return generators

# Unit Tests
class GetGeneratorsTest(unittest.TestCase):
    def testGetGenerators(self):
        # Test if the lenght of the returned list matches the parameter n
        for i in range(0, 20):
            self.assertTrue(len(GetGenerators(i)) == i)

        # Checking if all elements in the list are unique
        x = GetGenerators(50)
        self.assertFalse(len(x) > len(set(x)))


if __name__ == '__main__':
    unittest.main()
