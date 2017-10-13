import unittest
import gmpy2
from gmpy2 import mpz

from chvote.Utils.Utils       import AssertBytes
from chvote.Utils.ToByteArray import ToByteArray
from chvote.Utils.ToString    import ToString

def StringToInteger(S, A):
    """
    Algorithm 4.7: Computes a non-negative integer from a given string S.

    Args:
       S (str):     String
       A (list):    Alphabet

    Returns:
       mpz:         Integer
    """

    x = mpz(0)

    for i in range(len(S)):
        x += (len(A) ** (len(S) - 1 - i)) * (A.index(S[i]))

    return x

class StringToIntegerTest(unittest.TestCase):
    def testStringToInteger(self):
        A = ['0', '1'] # Alphabet
        k = 8
        x = mpz(5)
        self.assertEqual(ToString(x, k, A), ['0', '0', '0', '0', '0', '1', '0', '1'])

if __name__ == '__main__':
    unittest.main()
