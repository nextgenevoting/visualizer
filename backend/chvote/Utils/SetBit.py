import unittest

def SetBit(B, i, b):
    """

    Algorithm 4.2: Sets the i-th bit of a byte array B to b P B.

    Args:
        B1 (bytearray):     byte array
        m (int):            watermark
        m_max (int):        maximal watermark

    Returns:
        bytearray:          Watermarked bytearray
    """

    j = i // 8
    x = 2 ** (i % 8)

    if b == 0:
        B[j] = B[j]  & (255 - x)
    else:
        B[j] = B[j] | x

class SetBitTest(unittest.TestCase):
    def testSetBit(self):
        b = bytearray(b'\x08')
        SetBit(b, 1, 1)
        self.assertEqual(b, b'\x0A')
        SetBit(b, 1, 0)
        self.assertEqual(b, b'\x08')
        SetBit(b, 1, 0)

        b = bytearray(b'\x00\x00\x00')
        SetBit(b, 9, 1)
        self.assertEqual(b, b'\x00\x02\x00')

if __name__ == '__main__':
    unittest.main()
