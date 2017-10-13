import unittest
import gmpy2
from gmpy2 import mpz

from chvote.Utils.Utils       import AssertBytes
from chvote.Utils.ToByteArray import ToByteArray

def ToInteger(B):
    """
    Algorithm 4.5: Computes a non-negative integer from a given byte array B. Leading zeros of B are ignored.

    Args:
       B (bytes):   The bytearray to be converted to an integer

    Returns:
       int:         Integer
    """

    return int.from_bytes(B, byteorder='big')

class ToIntegerTest(unittest.TestCase):
    def testToInteger(self):
        self.assertEqual(123, ToInteger(ToByteArray(123)))
        self.assertEqual(mpz(123), ToInteger(ToByteArray(mpz(123))))
        self.assertEqual(ToInteger(b'\xff'), 255)

if __name__ == '__main__':
    unittest.main()
