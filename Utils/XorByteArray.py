import unittest

def XorByteArray(BS):
    """
    Helper function to xor multiple bytearrays of the same length!

    Args:
        BS (list):          List of bytearrays

    Returns:
        bytearray:          XOR'ed bytearray
    """

    assert len(BS) >= 2, "BS must be contain at least 2 bytearrays"

    byteArraySize = len(BS[0])
    res = bytearray(BS[0])

    for i in range(1, len(BS)):
        assert len(BS[i]) == byteArraySize, "All bytearrays must be of the same length!"

        for j in range(len(BS[i])):
            res[j] ^= BS[i][j]

    return res

class XorByteArrayTest(unittest.TestCase):
    def testXorByteArray(self):
        B = bytearray(b'\x0A')
        B2 = bytearray(b'\x05')
        res = XorByteArray([B, B2])
        self.assertEqual(res, b'\x0f')

if __name__ == '__main__':
    unittest.main()
