import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from IsMember import IsMember
from securityParameters import SECURITY_LEVEL_DEFAULT, SECURITY_LEVEL_0
from gmpy2 import mpz

# Unit Tests
class GetPrimesTest(unittest.TestCase):

    def testOne(self):
        self.assertTrue(IsMember(mpz(1)))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
