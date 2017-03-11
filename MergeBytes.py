import unittest

def MergeBytes(b1, b2):
    """
    Algorithm 4.2: Merges the bits of the two input bytes b1 and b2. The result
    is a byte array B of length 2. B[0] contains the four least significant from
    both b1 and b2, whereas B[1] contains the four most significant from both b1
    and b2 (in alternating order).

    @type  b1:  byte
    @param b1:  byte 1

    @type  b2:  byte
    @param b2:  byte 1

    @rtype:     bytearrarrayy
    @return:    bytearray
    """

    # For the better unterstanding of the algorithm, arithmetic operations
    # have been replaced with bit-wise operations:
    #
    # x << 1 | (y & 1)   instead of   2 * x + (y % 2)
    #      x >> 1        instead of    floor(x / 2)
    #
    # Numeric example:
    #
    # For for-loop:
    #
    #       b1      b2      b_1      b_2
    #   10101011 10010100 00000000 00000000
    # 0                   <<<<<<<<
    #          ^                 i
    #   >>>>>>>>
    #                     <<<<<<<<
    #                   ^        i
    #            >>>>>>>>
    #   01010101 01001010 00000010 00000000
    # 1                   <<<<<<<<
    #          ^                 i
    #   >>>>>>>>
    #                     <<<<<<<<
    #                   ^        i
    #            >>>>>>>>
    #   00101010 00100101 00001010 00000000
    # 2                   <<<<<<<<
    #          ^                 i
    #   >>>>>>>>
    #                     <<<<<<<<
    #                   ^        i
    #            >>>>>>>>
    #   00010101 00010010 00101001 00000000
    # 3                   <<<<<<<<
    #          ^                 i
    #   >>>>>>>>
    #                     <<<<<<<<
    #                   ^        i
    #            >>>>>>>>
    #   00001010 00001001 10100110 00000000
    #
    #
    # Second for-loop:
    #
    #       b1      b2      b_1      b_2
    #   00001010 00001001 10100110 00000000
    # 0                            <<<<<<<<
    #          ^                          i
    #   >>>>>>>>
    #                              <<<<<<<<
    #                   ^                 i
    #            >>>>>>>>
    #   00000101 00000100 10100110 00000001
    # 1                            <<<<<<<<
    #          ^                          i
    #   >>>>>>>>
    #                              <<<<<<<<
    #                   ^                 i
    #            >>>>>>>>
    #   00000010 00000010 10100110 00000110
    # 2                            <<<<<<<<
    #          ^                          i
    #   >>>>>>>>
    #                              <<<<<<<<
    #                   ^                 i
    #            >>>>>>>>
    #   00000001 00000001 10100110 00011000
    # 3                            <<<<<<<<
    #          ^                          i
    #   >>>>>>>>
    #                              <<<<<<<<
    #                   ^                 i
    #            >>>>>>>>
    #   00000000 00000000 10100110 01100011

    b_1 = 0

    for i in range(0, 4):
        b_1 = b_1 << 1 | (b1 & 1)
        b1 = b1 >> 1
        b_1 = b_1 << 1 | (b2 & 1)
        b2 = b2 >> 1

    b_2 = 0

    for i in range(0, 4):
        b_2 = b_2 << 1 | (b1 & 1)
        b1 = b1 >> 1
        b_2 = b_2 << 1 | (b2 & 1)
        b2 = b2 >> 1

    B = bytearray([b_1, b_2])

    return B

class MargeBytesTest(unittest.TestCase):
    def test(self):
        self.assertEqual(MergeBytes(0x00, 0x00), bytearray(b'\x00\x00')) # 00000000 00000000 -> 00000000 00000000
        self.assertEqual(MergeBytes(0xFF, 0xFF), bytearray(b'\xFF\xFF')) # 11111111 11111111 -> 11111111 11111111
        self.assertEqual(MergeBytes(0xFF, 0x00), bytearray(b'\xAA\xAA')) # 11111111 00000000 -> 10101010 10101010
        self.assertEqual(MergeBytes(0x00, 0xFF), bytearray(b'\x55\x55')) # 00000000 11111111 -> 01010101 01010101
        self.assertEqual(MergeBytes(0xAA, 0xAA), bytearray(b'\x33\x33')) # 10101010 10101010 -> 00110011 00110011
        self.assertEqual(MergeBytes(0x55, 0x55), bytearray(b'\xCC\xCC')) # 01010101 01010101 -> 11001100 11001100
        self.assertEqual(MergeBytes(0xF0, 0xF0), bytearray(b'\x00\xFF')) # 11110000 11110000 -> 00000000 11111111
        self.assertEqual(MergeBytes(0x0F, 0x0F), bytearray(b'\xFF\x00')) # 00001111 00001111 -> 11111111 00000000
        self.assertEqual(MergeBytes(0xF0, 0x0F), bytearray(b'\x55\xAA')) # 11110000 00001111 -> 01010101 10101010
        self.assertEqual(MergeBytes(0x0F, 0xF0), bytearray(b'\xAA\x55')) # 00001111 11110000 -> 10101010 01010101

if __name__ == '__main__':
    unittest.main()
