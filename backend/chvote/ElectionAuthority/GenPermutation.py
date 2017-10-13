import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils                    import AssertInt, AssertClass
from chvote.Types                          import *
from chvote.Utils.Random                   import randomBoundedInt
from chvote.Common.SecurityParams import SecurityParams, secparams_l3

def GenPermutation(N, secparams):
    """
    Algorithm 7.42: Generates a random permutation ψ ∈ Ψ following Knuth's shuffle algorithm.

    Args:
       N (int):                           Permutation size
       secparams (SecurityParams):          Collection of public security parameters

    Returns:
        list of int:                        Permutation
    """

    AssertInt(N)
    AssertClass(secparams, SecurityParams)


    I = list(range(N))
    res = []

    for i in range(N):
        k = randomBoundedInt(i,N-1, secparams)
        j_i = I[k]
        I[k] = I[i]

        res.append(j_i)

    return res

class GenPermutationTest(unittest.TestCase):
    def testGenPermutation(self):
        self.assertTrue(len(GenPermutation(10, secparams_l3)) == 10)
        self.assertTrue(len(GenPermutation(5, secparams_l3)) == 5)
        self.assertTrue(len(GenPermutation(0, secparams_l3)) == 0)

        for i in GenPermutation(100, secparams_l3):
            self.assertTrue(i >= 0 and i < 100)

if __name__ == '__main__':
    unittest.main()
