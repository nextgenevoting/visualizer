import gmpy2
from gmpy2 import mpz
import unittest
from SecurityContext import SECURITYCONTEXT_DEFAULT, SECURITYCONTEXT_L0
from Utils import ToInteger, AssertInt
from Crypto.IsMember import IsMember
from Crypto.RecHash import RecHash

def GetGenerators(n, ctx=SECURITYCONTEXT_DEFAULT):
    """
    Algorithm 7.3: Computes n independent generators of Gq. The algorithm is an adaption of the NIST standard FIPS PUB 186-4 [1, Appendix A.2.3].
    The string "chVote" guarantees that the resulting values are specific for chVote.

    @type   n:  int
    @param  n:  The number of primes to be calculated

    @rtype:     list
    @return:    a list with independent generators of G_p
    """
    AssertInt(n)

    generators = []

    for i in range(0, n):
        x = 0

        while True:
            x += 1
            h = mpz(ToInteger(RecHash(["chVote", i, x])) % ctx.p)
            h = (h ** 2) % ctx.p

            if h not in (0, 1, ctx.h, ctx.g) and h not in generators:
                break

        generators.append(h)

    return generators

# Unit Tests
class GetGeneratorsTest(unittest.TestCase):
    def testOne(self):
        # Test if the lenght of the returned list matches the parameter n
        for i in range(0, 20):
            self.assertTrue(len(GetGenerators(i)) == i)

        # Checking if all elements in the list are unique
        x = GetGenerators(50)
        self.assertFalse(len(x) > len(set(x)))

        # In the group G_281 (safeprime), the maximum number of unique generators we can get are 278:
        # print(len(GetGenerators(278)))

if __name__ == '__main__':
    unittest.main()
