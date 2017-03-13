import unittest

from Utils.MergeBytes import MergeBytes

def MergeByteArrays(B1, B2):
    """

    Algorithm 4.1: Merges the bytes of the two input byte arrays B1 and B2 pairwise.
    If one byte array is longer than the other, the additional bytes are attached to
    the result.

    Args:
        B1 (bytearray): byte array 1
        B2 (bytearray): byte array 2

    Returns:
        bytearray:      B1 and B2 merged
    """

    m = min(len(B1), len(B2))
    B = bytearray()

    for i in range(0, m):
        B = B + MergeBytes(B1[i], B2[i])

    B = B + B1[m:] + B2[m:]

    return B

class MergeByteArraysTest(unittest.TestCase):
    def test(self):
        self.assertEqual(MergeByteArrays(bytearray(b'\x00'), bytearray(b'\x00')), bytearray(b'\x00\x00'))
        self.assertEqual(MergeByteArrays(bytearray(b'\xFF'), bytearray(b'\xFF')), bytearray(b'\xFF\xFF'))
        self.assertEqual(MergeByteArrays(bytearray(b'\xFF'), bytearray(b'\x00')), bytearray(b'\xAA\xAA'))
        self.assertEqual(MergeByteArrays(bytearray(b'\x00'), bytearray(b'\xFF')), bytearray(b'\x55\x55'))

if __name__ == '__main__':
    unittest.main()
