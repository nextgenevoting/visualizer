import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils           import AssertInt, AssertClass, AssertList
from Types                 import *
from Common.SecurityParams import SecurityParams, secparams_l0, secparams_l3
from Common.GetPrimes      import GetPrimes
from Common.IsMember       import IsMember

def GetVotes(m_bold, n, secparams):
    """
    Algorithm 7.54: Computes the election result matrix V = (v_ij) N x n from the products
    of encoded selections m = (m_1, ..., m_N) by retrieving the prime factors of each mi.
    Each resulting vector vi represents somebody’s vote, and each value vij  1 represents
    somebody’s vote for a specific candidate j in {1, ..., n}

    Args:
       m_bold (List):                       Products of encoded selections m = (m_1, ..., m_N), m_i in G_q
       n (int):                             Number of candidates n >= 2
       secparams (SecurityParams):          Collection of public security parameters

    Returns:
        list of int:                        Election result matrix V = (v_ij) N x n
    """

    AssertList(m_bold)
    for m in m_bold: assert IsMember(m, secparams), "m_bold elements must be in G_q"
    AssertInt(n)
    assert n >= 2, "n must be greater than or equal 2"
    AssertClass(secparams, SecurityParams)

    V_bold = []
    N = len(m_bold)

    p_bold = GetPrimes(n, secparams)
    for i in range(N):
        v_bold_i = [None] * n
        for j in range(n):
            if m_bold[i] % p_bold[j] == 0:
                v_bold_i[j] = 1
            else:
                v_bold_i[j] = 0
        V_bold.append(v_bold_i)

    return V_bold

class GetVotesTest(unittest.TestCase):
    def testGetVotes(self):
        # Testing is done with integration tests
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
