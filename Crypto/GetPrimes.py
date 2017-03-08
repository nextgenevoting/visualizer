import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import gmpy2
from gmpy2 import mpz
from SecurityParams import secparams_def, secparams_l0, secparams_l3
from Crypto.IsMember import IsMember
from Utils import AssertInt

def GetPrimes(n, secparams=secparams_def):
    """
    Algorithm 7.1: Computes the first n prime numbers from Gq. The computation possibly
    fails if n is large and p is small, but this case is very unlikely in practice. In a more
    efficient implementation of this algorithm, the resulting list of primes is precomputed for
    the largest expected value n.

    @type   n:  int
    @param  n:  Number of primes to be calculated

    @rtype:     list
    @return:    a list with length n containing the first n prime numbers in G_p
    """
    AssertInt(n)

    x = 1
    primes = []

    for i in range(0, n):                                # i = 0, ... , n-1
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

    def testTwo(self):
        # Test the case of n = 0
        self.assertTrue(len(GetPrimes(0)) == 0)

    def testPrimesForSecurityLevel0(self):
        # test if the 50 first primes of group G_563 (this corresponds to security level Lambda = 0) are correct
        # according to table 8.2 in the specification document
        primes = GetPrimes(50, secparams_l0)
        self.assertTrue(primes[0] == 3)
        self.assertTrue(primes[1] == 7)
        self.assertTrue(primes[2] == 11)
        self.assertTrue(primes[3] == 13)
        self.assertTrue(primes[4] == 17)
        self.assertTrue(primes[5] == 19)
        self.assertTrue(primes[6] == 23)
        self.assertTrue(primes[7] == 47)
        self.assertTrue(primes[8] == 59)
        self.assertTrue(primes[9] == 61)
        self.assertTrue(primes[10] == 67)
        self.assertTrue(primes[11] == 71)
        #.....
        self.assertTrue(primes[49] == 541)

    def testPrimesForSecurityLevel3(self):
        # test if the 50 first primes of group G_p for security level 3 are correct
        # according to table 8.12 in the specification document
        primes = GetPrimes(50, secparams_l3)
        print(primes)
        self.assertTrue(primes[0] == 2)
        self.assertTrue(primes[1] == 3)
        self.assertTrue(primes[2] == 7)
        self.assertTrue(primes[3] == 11)
        self.assertTrue(primes[4] == 31)
        self.assertTrue(primes[5] == 43)
        self.assertTrue(primes[6] == 47)
        self.assertTrue(primes[7] == 59)
        self.assertTrue(primes[8] == 67)
        self.assertTrue(primes[9] == 71)
        self.assertTrue(primes[10] == 79)
        self.assertTrue(primes[11] == 83)
        #.....
        self.assertTrue(primes[49] == 601)

if __name__ == '__main__':
    unittest.main()
