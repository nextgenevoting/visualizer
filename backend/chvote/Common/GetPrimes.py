import gmpy2
import os
import sys
import unittest
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils           import AssertInt, AssertClass
from chvote.Common.SecurityParams import secparams_l0, secparams_l1, secparams_l2, secparams_l3, SecurityParams
from chvote.Common.IsMember       import IsMember

def GetPrimes(n, secparams):
    """
    Algorithm 7.1: Computes the first n prime numbers from G_q. The computation possibly
    fails if n is large and p is small, but this case is very unlikely in practice. In a more
    efficient implementation of this algorithm, the resulting list of primes is precomputed for
    the largest expected value n.

    Args:
       n (int):                             Number of primes to be calculated
       secparams (SecurityParams):          Collection of public security parameters

    Returns:
       list of mpz :                        A list with length n containing the first n prime numbers in G_p
    """

    AssertInt(n)
    AssertClass(secparams, SecurityParams)

    x = mpz(1)
    primes = []

    for i in range(n):                                # i = 0, ... , n-1
        while True:
            x += 1 if x <= 2 else mpz(2)

            if x >= secparams.p:
                return []                                # n is incompatible with p
            if gmpy2.is_prime(x) and IsMember(x, secparams):   # see Alg. 7.2
                break

        primes.append(x)

    return primes                                        # p \elementof G_p \cap P)^n

class GetPrimesTest(unittest.TestCase):
    def testOne(self):
        # Test if the lenght of the returned list matches the parameter n
        self.assertTrue(len(GetPrimes(10, secparams_l3)) == 10)

    def testPrimesForSecurityLevel0(self):
        # Test whether the 50 first primes of group G_563 (this corresponds to
        # security level Lambda = 0) are correct according to table 8.2 in the
        # specification document.

        primes = GetPrimes(50, secparams_l0)
        for i, p in enumerate([mpz(3), mpz(13), mpz(19), mpz(23), mpz(29), mpz(37), mpz(43), mpz(59), mpz(71), mpz(83),
                          mpz(97), mpz(107), mpz(109), mpz(113), mpz(149), mpz(163), mpz(173), mpz(179), mpz(181),
                          mpz(229), mpz(233), mpz(239), mpz(251), mpz(257), mpz(269), mpz(271), mpz(277), mpz(281),
                          mpz(283), mpz(293), mpz(307), mpz(311), mpz(317), mpz(331), mpz(347), mpz(349), mpz(367),
                          mpz(373), mpz(383), mpz(401), mpz(409), mpz(419), mpz(421), mpz(431), mpz(433), mpz(439),
                          mpz(443), mpz(449), mpz(499), mpz(509)]):
            self.assertEqual(primes[i], p)

    def testPrimesForSecurityLevel1(self):
        # Test whether the 50 first primes of group G_p for security level 1
        # are correct according to table 8.5 in the specification document.

        primes = GetPrimes(50, secparams_l1)

        for i, p in enumerate( [mpz(3), mpz(5), mpz(7), mpz(11), mpz(13), mpz(23), mpz(29), mpz(41), mpz(43), mpz(47), mpz(59), mpz(79), mpz(83), mpz(89), mpz(101), mpz(103), mpz(109), mpz(131), mpz(137), mpz(149), mpz(151), mpz(157), mpz(179), mpz(181), mpz(199), mpz(227), mpz(229), mpz(239), mpz(241), mpz(251), mpz(263), mpz(269), mpz(271), mpz(277), mpz(281), mpz(283), mpz(293), mpz(317), mpz(337), mpz(347), mpz(353), mpz(367), mpz(373), mpz(379), mpz(383), mpz(409), mpz(419), mpz(431), mpz(443), mpz(449)]):
            self.assertEqual(primes[i], p)


if __name__ == '__main__':
    unittest.main()
