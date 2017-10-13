import unittest
import gmpy2
from gmpy2 import mpz

from chvote.Utils.Utils import AssertNumeric, AssertInt

def ToByteArray(x):
    """
    Algorithm 4.3: ToByteArray(x): Converts the given integer to a bytearray in big-endian byte order

    Args:
       x (int | mpz):       The number to be converted to a bytearray

    Returns:
       bytes:       Immutable bytearray in big-endian byte order
    """

    # this seems faster than the original code:
    x = int(x)  # convert mpz to int because mpz has no .to_bytes method
    return x.to_bytes((x.bit_length() + 7) // 8, byteorder='big')

    # Alternative without floating-point operations:
    #q, r = divmod(BitAbs(x), 8)
    #q += bool(r)

    #return ToByteArrayN(x, q)

def ToByteArrayN(x, n):
    """
    Algorithm 4.4: ToByteArrayN(x, n): Converts the given integer to a bytearray of size n in big-endian byte order

    Args:
       x (int | mpz):       The number to be converted into an array of bytes
       n (int):             length of the output bytearray

    Returns:
       bytes:       Immutable bytearray of size n in big-endian byte order
    """
    AssertNumeric(x)
    n = int(n)

    x = int(x)      # convert mpz to int because mpz has no .to_bytes method
    return x.to_bytes(n, byteorder='big')

    #B = bytearray(n)

    #for i in range(n):
    #    b = x % 256
    #    x = x // 256                  # // = integer division => floor
    #    B.insert(0, b)

    #return bytes(B)

class UtilsTest(unittest.TestCase):
    def testToByteArray(self):
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
        self.assertTrue(ToByteArray(0) == bytearray(b''))

        self.assertTrue(ToByteArray(1) == bytearray(b'\x01'))

        self.assertTrue(ToByteArray(255) == bytearray(b'\xff'))

        self.assertTrue(ToByteArray(256) == bytearray(b'\x01\x00'))

        self.assertTrue(ToByteArray(65535) == bytearray(b'\xff\xff'))

        self.assertTrue(ToByteArray(65536) == bytearray(b'\x01\x00\x00'))

        self.assertTrue(ToByteArray(16777215) == bytearray(b'\xff\xff\xff'))

        self.assertTrue(ToByteArray(16777216) == bytearray(b'\x01\x00\x00\x00'))

    def testToByteArrayN(self):
        print(ToByteArrayN(0, 0), bytearray(b''))
        print(ToByteArrayN(0, 1), bytearray(b'\x00'))
        print(ToByteArrayN(0, 2), bytearray(b'\x00\x00'))

if __name__ == '__main__':
    unittest.main()
