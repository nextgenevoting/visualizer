import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from GetPrimes import GetPrimes
from SecurityContext import SECURITYCONTEXT_L0


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
        primes = GetPrimes(50, SECURITYCONTEXT_L0)
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
