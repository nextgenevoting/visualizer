import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from Utils import ToByteArray, bit_abs
from SecurityContext import SECURITYCONTEXT_L0
import gmpy2
from gmpy2 import mpz

# Unit Tests
class UtilsTest(unittest.TestCase):

    def testBitAbs(self):     
        print(bit_abs(2**16))
        # some value tests
        self.assertTrue(bit_abs(2**16) == 17)
        self.assertTrue(bit_abs(2**16-1) == 16)
        # negative value tests
        self.assertTrue(bit_abs(-2**16) == 17)
        # zero
        self.assertTrue(bit_abs(0) == 0)
        
    def testByteArray(self):        
        # test conversion of an mpz
        bx = ToByteArray(mpz(255))
        self.assertTrue(bx == bytearray(b'\xff'))

        # test conversion of a python integer
        bx = ToByteArray(255)
        self.assertTrue(bx == bytearray(b'\xff'))

        # test length of a larger int
        bx = ToByteArray(65536)
        self.assertTrue(len(bx) == 3)   # len(65536) = len(00000001 00000000 00000000) = 3
 
        # test length of a larger mpz
        bx = ToByteArray(mpz(2**4096))
        print(bx)
        self.assertTrue(len(bx) == 513)   # len(2^4096) = 513


def main():
    unittest.main()   

if __name__ == '__main__':
    main()
