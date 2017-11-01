import unittest
import gmpy2
from gmpy2 import mpz
from math import ceil, floor, log2
from array import array

# Assertions
# Important: type() is very slow! use isinstance() instead!

def AssertNumeric(i):
    assert isinstance(i, int) or i.__class__.__name__ == 'mpz', 'Expected nummeric value!'

def AssertInt(i):
    assert isinstance(i, int), 'Expected int!'

def AssertMpz(i):
    assert i.__class__.__name__ == 'mpz', 'Expected mpz!'

def AssertBytes(B):
    assert B.__class__.__name__ == 'bytes' ,'Expected bytes!'

def AssertList(V):
    assert isinstance(V, list), 'Expected list!'

def AssertTuple(V):
    assert isinstance(V, tuple), 'Expected tuple!'

def AssertClass(c, type):
    assert isinstance(c, type), 'Expected class %s' % type
    #return

def AssertString(s):
    assert isinstance(s, str), "Expected string"

def isNumericType(i):
    return isinstance(i, int) or i.__class__.__name__ == 'mpz'

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

def Skip(B, l):
    """
    Helper function to skip a bytearray to the given length

    Args:
       B (bytes):   The bytes to be converted to an integer
       l (int):     Length

    Returns:
       bytearray:   Bytearray skipped to length
    """

    return B[l:len(B)]

class UtilsTest(unittest.TestCase):
    def testBitAbs(self):
        # some value tests
        self.assertTrue(BitAbs(2 ** 16) == 17)
        self.assertTrue(BitAbs(2 ** 16 - 1) == 16)
        # negative value tests
        self.assertTrue(BitAbs(-2 ** 16) == 17)
        # zero
        self.assertTrue(BitAbs(0) == 0)

    def testTruncate(self):
        B = bytearray(b'0123456789')

        for i in range(10):
            self.assertEqual(Truncate(B, i) + Skip(B,i), B)

if __name__ == '__main__':
    unittest.main()
