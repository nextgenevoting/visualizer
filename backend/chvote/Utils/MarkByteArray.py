import unittest

from chvote.Utils.Utils  import BitAbs
from chvote.Utils.SetBit import SetBit
from math         import floor

def MarkByteArray(B, m, m_max):
    """

   Algorithm 4.1: Adds an integer watermark m to the bits of a given byte array. The bits
   of the watermark are spread equally across the bits of the byte array.

    Args:
        B1 (bytearray):     byte array
        m (int):            watermark
        m_max (int):        maximal watermark

    Returns:
        bytearray:          Watermarked bytearray
    """

    l = BitAbs(m_max)
    s = (8 * len(B)) // l

    assert l <= 8 * len(B), "||m_max|| <= 8 * |B|"

    for i in range(l):
        SetBit(B, floor(i*s), m % 2)
        m = m // 2

    return B

class MarkByteArrayTest(unittest.TestCase):
    def testMarkByteArray(self):
        B = bytearray(b'\x01\x01\x01\x01\x01')
        B2 = MarkByteArray(B, 55, 100)
        print(B2)

if __name__ == '__main__':
    unittest.main()
