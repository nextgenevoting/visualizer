import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils           import AssertInt, AssertClass, AssertList
from Types                 import *
from Utils.Random          import randomMpz
from Crypto.SecurityParams import SecurityParams, secparams_l0, secparams_l3
from Crypto.GetPrimes      import GetPrimes

def GetVotes(m_bold, n, secparams):
    """
    Algorithm 7.54: Computes the election result matrix V = (v_ij) N x n from the products
    of encoded selections m = (m_1, ..., m_N) by retrieving the prime factors of each mi.
    Each resulting vector vi represents somebody’s vote, and each value vij  1 represents
    somebody’s vote for a specific candidate j in {1, ..., n}

    Args:
       m_bold (List):       Products of encoded selections m
       n (int):             Number of candidates n >= 2

    Returns:
        list                Partial decryptions
    """

    AssertList(m_bold)
    AssertInt(n)
    AssertClass(secparams, SecurityParams)

    p_bold = GetPrimes(n, secparams)

    V_bold = []
    for i in range(len(m_bold)):
        v_bold_i = []
        for j in range(n):
            if m_bold[i] % p_bold[j] == 0:
                v_bold_i.append(1)
            else:
                v_bold_i.append(0)
        V_bold.append(v_bold_i)

    return V_bold

class GetVotesTest(unittest.TestCase):
    def testGetVotes(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
