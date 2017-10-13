import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Common.SecurityParams import SecurityParams, secparams_l0
from chvote.Common.GetPrimes      import GetPrimes
from chvote.Utils.Utils           import AssertList, AssertClass

def GetSelectedPrimes(s_bold, secparams):
    """
    Algorithm 7.19: Selects k prime numbers from Gq corresponding to the given
    indices s = (s_1, ..., s_k). For example, s = (1, 3, 7) means selecting the
    first, the third, and the seventh prime from G_q.

    Args:
        s_bold (list of int):                Selections
        secparams (SecurityParams):          Collection of public security parameters

    Returns:
        list of mpz:                         List of the selected prime numbers
    """

    AssertList(s_bold)
    AssertClass(secparams, SecurityParams)

    s_k = max(s_bold)+1
    p_bold = GetPrimes(s_k, secparams)
    q_bold = [ p_bold[s_i] for s_i in s_bold ]

    return q_bold

class GetSelectedPrimesTest(unittest.TestCase):
    def testGetSelectedPrimesL0(self):
        self.assertEqual(GetSelectedPrimes([1, 2], secparams_l0), [7, 11])
        self.assertEqual(GetSelectedPrimes([3, 1], secparams_l0), [11, 3])
        self.assertEqual(GetSelectedPrimes([0, 1], secparams_l0), [2, 3])
        self.assertEqual(GetSelectedPrimes([0, 1, 2], secparams_l0), [2, 3, 7])

if __name__ == '__main__':
    unittest.main()
