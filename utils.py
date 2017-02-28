import unittest

import gmpy2
from gmpy2 import mpz
from math import ceil, floor, log2
from array import array

def bit_abs(i):
    """
    This algorithm implements the ||i|| operator used in the specification document, defined on page 11

    @type   i:  number
    @param  i:  The number to get the absolute value of

    @rtype:     int
    @return:    absolute bit length of i
    """
              
    # return math.floor(math.log2(abs(i)))+1
    # Alternative without floating-point operations:
    return i.bit_length() 


def ToByteArray(x):
    """
    Converts the given integer to a bytearray in big-endian byte order

    @type   x   integer | mpz
    @param  x:  The number to be converted to a bytearray

    @rtype:     bytearay
    @return:    Bytearray in big-endian byte order
    """

    # n_min = ceil(bit_abs(x)/8)
    # Alternative without floating-point operations:
    q,r = divmod(bit_abs(x),8)
    q += bool(r)

    return ToByteArrayN(x, q)

def ToByteArrayN(x, n):
    """
    Converts the given integer to a bytearray of size n in big-endian byte order

    @type   x   integer | mpz
    @param  x:  The number to be converted into an array of bytes

    @type   n   integer
    @param  n:  length of the output bytearray

    @rtype:     bytearray
    @return:    Bytearray of size n in big-endian byte order
    """
    B = bytearray()
    for i in range(0,int(n)):        
        b = x % 256
        x = x // 256                  # // = integer division => floor
        B.insert(0,b)
    return B


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
        self.assertTrue(len(bx) == 513)   # len(2^4096) = 513

        # test all the cases of table 4.1 in the specification document
        print(ToByteArray(0))        
        self.assertTrue(ToByteArray(0) == bytearray(b''))
   
        print(ToByteArray(1))        
        self.assertTrue(ToByteArray(1) == bytearray(b'\x01'))
    
        print(ToByteArray(255))        
        self.assertTrue(ToByteArray(255) == bytearray(b'\xff'))

        print(ToByteArray(256))        
        self.assertTrue(ToByteArray(256) == bytearray(b'\x01\x00'))

        print(ToByteArray(65535))        
        self.assertTrue(ToByteArray(65535) == bytearray(b'\xff\xff'))

        print(ToByteArray(65536))        
        self.assertTrue(ToByteArray(65536) == bytearray(b'\x01\x00\x00'))
        
        print(ToByteArray(16777215))        
        self.assertTrue(ToByteArray(16777215) == bytearray(b'\xff\xff\xff'))
        
        print(ToByteArray(16777216))        
        self.assertTrue(ToByteArray(16777216) == bytearray(b'\x01\x00\x00\x00'))


def main():
    unittest.main()   

if __name__ == '__main__':
    main()
