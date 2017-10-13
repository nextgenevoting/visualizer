import unittest
import gmpy2
import os, sys
from gmpy2 import mpz
from math import ceil, log2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.ToInteger import ToInteger
from chvote.Utils.Utils     import AssertMpz, AssertInt, AssertList

def ByteArrayToString(B, A):
    """
    Algorithm 4.8: Computes the shortest string representation fo a given byte Array B relative to some alphabet A

    Args:
       B (bytearray):   Bytearray
       A (list)         Alphabet A = {c_1, ..., c_N}

    Returns:
       string:      The string representation of x
    """

    x_B = mpz(ToInteger(B))
    k = ceil((8 * len(B)) / log2(len(A)))

    return ToString(x_B, k, A)

def ToString(x, k, A):
    """
    Algorithm 4.6: Computes a string representation of length k in big-endian order of a given non negative integer x in N

    Args:
       x (mpz):     Integer x ∈ N
       k (int)      String length k >= log_N (x)
       A (list)     Alphabet A = {c_1, ..., c_N}

    Returns:
       string:      The string representation of x
    """

    AssertMpz(x)
    AssertInt(k)
    AssertList(A)

    S = ""
    N = len(A)

    for i in reversed(range(k)):
        s_k = A[x % N]
        x = x // N
        S = s_k + S

    return S

class ToStringTest(unittest.TestCase):
    def testToString(self):
        A = ['0', '1'] # Alphabet
        k = 8
        x = mpz(5)
        self.assertEqual(ToString(x, k, A), ['0', '0', '0', '0', '0', '1', '0', '1'])

        B = b'\xff'
        s = ByteArrayToString(B, ['0', '1','2', '3', '4', '5', '6', '7', '8','9'])
        self.assertEqual(s, ['2', '5', '5'])

if __name__ == '__main__':
    unittest.main()
