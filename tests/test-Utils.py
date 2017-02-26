import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from utils import ToByteArray
from SecurityContext import SECURITYCONTEXT_L0
import gmpy2
from gmpy2 import mpz

# Unit Tests
class ToByteArrayTest(unittest.TestCase):

    def testOne(self):
        x = mpz(5)
        print(ToByteArray(x))

 
def main():
    unittest.main()   

if __name__ == '__main__':
    main()
