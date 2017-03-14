import unittest
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Crypto.SecurityParams  import secparams_default, secparams_l0
from Crypto.GetPrimes       import GetPrimes

def GetSelectedPrimes(s, secparams=secparams_default):
    """
    Algorithm 7.19: Selects k prime numbers from Gq corresponding to the given
    indices s = (s_1, ..., s_k). For example, s = (1, 3, 7) means selecting the
    first, the third, and the seventh prime from G_q.

    Args:
        s (list):   Selections

    Returns:
        list:       List of the selected prime numbers
    """

    s_k = max(s) if len(s) > 0 else 0
    p = GetPrimes(s_k)
    q = [ p[s_i - 1] for s_i in s ]

    return q

class GetSelectedPrimesTest(unittest.TestCase):
    def testGetSelectedPrimesL0(self):
        self.assertEqual(GetSelectedPrimes([], secparams_l0), [])
        self.assertEqual(GetSelectedPrimes([1], secparams_l0), [2])
        self.assertEqual(GetSelectedPrimes([3], secparams_l0), [7])
        self.assertEqual(GetSelectedPrimes([1, 2], secparams_l0), [2, 3])
        self.assertEqual(GetSelectedPrimes([1, 2, 3], secparams_l0), [2, 3, 7])

if __name__ == '__main__':
    unittest.main()
