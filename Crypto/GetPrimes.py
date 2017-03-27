import unittest
import os, sys
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils            import AssertInt, AssertClass
from Crypto.SecurityParams  import secparams_default, secparams_l0, secparams_l1, secparams_l2, secparams_l3, SecurityParams
from Crypto.IsMember        import IsMember

def GetPrimes(n, secparams=secparams_default):
    """
    Algorithm 7.1: Computes the first n prime numbers from G_q. The computation possibly
    fails if n is large and p is small, but this case is very unlikely in practice. In a more
    efficient implementation of this algorithm, the resulting list of primes is precomputed for
    the largest expected value n.

    Args:
       n (int):     Number of primes to be calculated

    Returns:
       list:        A list with length n containing the first n prime numbers in G_p
    """

    AssertInt(n)
    assert n >= 2, "n must be greater or equal 2"
    AssertClass(secparams, SecurityParams)

    x = 1
    primes = []

    for i in range(n):                                # i = 0, ... , n-1
        while True:
            x += 1 if x <= 2 else 2

            if x >= secparams.p:
                return []                                # n is incompatible with p
            if gmpy2.is_prime(x) and IsMember(x, secparams):   # see Alg. 7.2
                break

        primes.append(x)

    return primes                                        # p \elementof G_p \cap P)^n

# Unit Tests
class GetPrimesTest(unittest.TestCase):
    def testOne(self):
        # Test if the lenght of the returned list matches the parameter n
        self.assertTrue(len(GetPrimes(10)) == 10)

    def testPrimesForSecurityLevel0(self):
        # Test whether the 50 first primes of group G_563 (this corresponds to
        # security level Lambda = 0) are correct according to table 8.2 in the
        # specification document.

        primes = GetPrimes(50, secparams_l0)

        for i, p in enumerate([   3,   7,  11,  13,  17,  19,  23,  47,  59,  61
                              ,  67,  71, 101, 103, 107, 113, 127, 137, 149, 179
                              , 181, 191, 193, 197, 211, 223, 241, 251, 257, 269
                              , 271, 277, 281, 337, 347, 349, 379, 383, 401, 409
                              , 421, 439, 449, 461, 467, 491, 503, 509, 521, 541
                              ]):
            self.assertEqual(primes[i], p)

    def testPrimesForSecurityLevel1(self):
        # Test whether the 50 first primes of group G_p for security level 1
        # are correct according to table 8.5 in the specification document.

        primes = GetPrimes(50, secparams_l1)

        for i, p in enumerate([   2,   3,  11,  23,  29,  47,  53,  67,  71,  83
                              ,  89,  97, 101, 113, 127, 151, 163, 173, 191, 193
                              , 197, 199, 211, 227, 229, 239, 251, 263, 269, 277
                              , 281, 307, 311, 313, 331, 367, 379, 389, 409, 433
                              , 439, 457, 479, 491, 509, 521, 523, 541, 547, 577
                              ]):
            self.assertEqual(primes[i], p)

    def testPrimesForSecurityLevel2(self):
        # Test whether the 50 first primes of group G_p for security level 2
        # are correct according to table 8.8 in the specification document.

        primes = GetPrimes(50, secparams_l2)

        for i, p in enumerate([   2,   3,   5,   7,  13,  19,  29,  31,  41,  47
                              ,  53,  59,  61,  79,  89,  97, 113, 127, 131, 137
                              , 139, 149, 151, 191, 193, 199, 211, 229, 263, 283
                              , 293, 307, 311, 317, 331, 337, 359, 373, 383, 397
                              , 401, 409, 419, 421, 431, 439, 443, 449, 467, 479
                              ]):
                self.assertEqual(primes[i], p)

    def testPrimesForSecurityLevel3(self):
        # Test whether the 50 first primes of group G_p for security level 3
        # are correct according to table 8.12 in the specification document.

        primes = GetPrimes(50, secparams_l3)

        for i, p in enumerate([   2,   3,   7,  11,  31,  43,  47,  59,  67,  71
                              ,  79,  83, 101, 103, 107, 109, 127, 151, 157, 197
                              , 211, 223, 227, 229, 233, 251, 271, 283, 293, 307
                              , 367, 373, 383, 419, 421, 431, 443, 449, 461, 463
                              , 467, 491, 499, 503, 521, 523, 547, 563, 577, 601
                              ]):
                self.assertEqual(primes[i], p)

if __name__ == '__main__':
    unittest.main()
