import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from GetPrimes import RecHash
from SecurityContext import SECURITYCONTEXT_L0


# Unit Tests
class RecHashTest(unittest.TestCase):

    def testOne(self):
        self.assertTrue(len(RecHash([])))
        

def main():
    unittest.main()   

if __name__ == '__main__':
    main()
