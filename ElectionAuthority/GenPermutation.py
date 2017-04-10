import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                        import AssertInt
from Types                              import *
from Utils.Random                       import randomBoundedInt

def GenPermutation(N):
    """
    Algorithm 7.42: Generates a random permutation  P 	N following Knuth’s shuffle algorithm [15, pp. 139–140].

    Args:
       N (int):     Permutation size

    Returns:
        list
    """
    AssertInt(N)

    I = list(range(N))

    res = []
    for i in range(N):
        k = randomBoundedInt(i,N-1)
        j_i = I[k]
        I[k] = I[i]

        res.append(j_i)

    return res


class GenPermutationTest(unittest.TestCase):
    def testGenPermutation(self):
        self.assertTrue(len(GenPermutation(10)) == 10)
        self.assertTrue(len(GenPermutation(5)) == 5)
        self.assertTrue(len(GenPermutation(0)) == 0)

        for i in GenPermutation(100):
            self.assertTrue(i >= 0 and i < 100)

if __name__ == '__main__':
    unittest.main()
