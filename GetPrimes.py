import securityParameters
from securityParameters import SECURITY_LEVEL_DEFAULT, SECURITY_LEVEL_0
import gmpy2
from gmpy2 import mpz
from IsMember import IsMember
import unittest


def GetPrimes(n, SECURITYPARAMS = SECURITY_LEVEL_DEFAULT):
    """
    Algorithm 7.1: Computes the first n prime numbers from Gq. The computation possibly
    fails if n is large and p is small, but this case is very unlikely in practice. In a more
    efficient implementation of this algorithm, the resulting list of primes is precomputed for
    the largest expected value n.

    @type   n:  number
    @param  n:  The number of primes to be calculated
    @type   p:  number
    @param  p:  The order of the group G_p (defaults to the specified security level parameters)

    @rtype:     list
    @return:    a list with length n containing the first n prime numbers in G_p
    """
    x = mpz(1)
    primes = []
    for i in range(n):
        while True:
            if x <= 2:
                x += 1
            else:
                x += 2

            if x >= SECURITYPARAMS.p:
                return []                           # n is incompatible with p
            if gmpy2.is_prime(x) and IsMember(x):   # see Alg. 7.2
                break
        primes.append(x)
    
    return primes                                   # p \elementof G_p \cap P)^n
    
# Unit Tests
class GetPrimesTest(unittest.TestCase):

    def testOne(self):
        # Test if the lenght of the returned list matches the parameter n
        self.assertTrue(len(GetPrimes(10)) == 10)

    def testTwo(self):
        # Test the case of n = 0
        self.assertTrue(len(GetPrimes(0)) == 0)

    def testPrimesForLambdaZero(self):
        # test if the 50 first primes of group G_563 (this corresponds to security level Lambda = 0) are correct
        # according to table 8.2 in the specification document
        primes = GetPrimes(50, SECURITY_LEVEL_0)
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


def main():
    #unittest.main()
    print(GetPrimes(50))

if __name__ == '__main__':
    main()
