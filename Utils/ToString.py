import unittest
import gmpy2
from gmpy2 import mpz

from Utils.Utils import AssertMpz, AssertInt, AssertList

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
    N = len(A)

    for i in reversed(range(0, k)):
        s_k = A[x % N]
        x = x // N
        S.insert(0, s_k)

    return S

class ToStringTest(unittest.TestCase):
    def testToString(self):
        A = ['0', '1'] # Alphabet
        k = 8
        x = mpz(5)
        self.assertEqual(ToString(x, k, A), ['0', '0', '0', '0', '0', '1', '0', '1'])

if __name__ == '__main__':
    unittest.main()
