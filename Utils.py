import unittest
import gmpy2
from gmpy2 import mpz
from math import ceil, floor, log2
from array import array

# Assertions
# Important: type() is very slow! use isinstance() instead!

def AssertNummeric(i):
    assert isinstance(i,int) or i.__class__.__name__ == 'mpz', 'Expected nummeric value!'

def AssertInt(i):
    assert isinstance(i,int), 'Expected int!'

def AssertMpz(i):
    assert i.__class__.__name__ == 'mpz', 'Expected mpz!'

def AssertBytes(B):
    assert B.__class__.__name__ == 'bytes' ,'Expected bytearray!'

def AssertList(V):
    assert isinstance(V,list), 'Expected list!'

# Type checks

def isNummericType(i):
    return (isinstance(i,int) or i.__class__.__name__ == 'mpz')

# CHVote helper methods

def BitAbs(i):
    """
    This algorithm implements the ||i|| operator used in the specification document, defined on page 11

    Args:
       i (int | mpz):      The number to get the absolute value of

    Returns:
       int:     absolute bit length of i
    """

    # return math.floor(math.log2(abs(i)))+1
    # Alternative without floating-point operations:

    return i.bit_length()


def ToByteArray(x):
    """
    Algorithm 4.3: ToByteArray(x): Converts the given integer to a bytearray in big-endian byte order

    Args:
       x (int | mpz):       The number to be converted to a bytearray

    Returns:
       bytes:       Immutable bytearray in big-endian byte order
    """
    # this seems faster than the original code:
    x = int(x)
    return x.to_bytes((x.bit_length() + 7) // 8, byteorder='big')
   
    # Alternative without floating-point operations:
    #q, r = divmod(BitAbs(x),8)
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

    B = bytearray(n)

    for i in range(0, int(n)):
        b = x % 256
        x = x // 256                  # // = integer division => floor
        B.insert(0, b)

    return bytes(B)

def ToInteger(B):
    """
    Algorithm 4.5: Computes a non-negative integer from a given byte array B. Leading zeros of B are ignored.

    Args:
       B (bytes):   The bytearray to be converted to an integer

    Returns:
       int:         Integer
    """
    AssertBytes(B)

    return int.from_bytes(B, byteorder='big')

def ToString(x, k, A):
    """
    Algorithm 4.6: Computes a string representation of length k in big-endian order of a given non negative integer x in N

    Args:
       x (mpz):     Integer x in N
       k (int)      String length k >= log_N (x)
       A (list)     Alphabet A = {c_1, ..., c_N}

    Returns:
       string:      The string representation of x
    """
    AssertMpz(x)
    AssertInt(k)
    AssertList(A)

    S = []
    N = len(A)  # N = |A|

    for i in reversed(range(0,k)):
        s_k = A[x % N]
        x = x // N
        S.insert(0,s_k)

    return S



def Truncate(B, l):
    """
    Helper function to truncate a bytearray to the given length

    Args:
       B (bytes):   The bytes to be converted to an integer
       l (int):     Length

    Returns:
       bytearray:   Bytearray truncated to length    
    """

    return B[0:l]

# Unit Tests
class UtilsTest(unittest.TestCase):
    def testBitAbs(self):
        # some value tests
        self.assertTrue(BitAbs(2**16) == 17)
        self.assertTrue(BitAbs(2**16-1) == 16)
        # negative value tests
        self.assertTrue(BitAbs(-2**16) == 17)
        # zero
        self.assertTrue(BitAbs(0) == 0)

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


    def testToInteger(self):
        self.assertTrue(123 == ToInteger(ToByteArray(123)))
        self.assertTrue(mpz(123) == ToInteger(ToByteArray(mpz(123))))

    def testToString(self):
        A = ['0', '1']   # Alphabet
        k = 8
        x = mpz(5)
        S = ToString(x,k,A)
        print(S)


if __name__ == '__main__':
    unittest.main()
