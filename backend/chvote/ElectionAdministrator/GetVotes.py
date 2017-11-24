import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils           import AssertClass, AssertList
from chvote.Types                 import *
from chvote.Common.SecurityParams import SecurityParams
from chvote.Common.GetPrimes      import GetPrimes
from chvote.Common.IsMember       import IsMember

def GetVotes(m_bold, n_bold, w_bold, secparams):
    """
    Algorithm 7.54: Computes the election result matrix V = (v_ij) N x n from the products
    of encoded selections m = (m_1, ..., m_N) by retrieving the prime factors of each mi.
    Each resulting vector vi represents somebody’s vote, and each value vij  1 represents
    somebody’s vote for a specific candidate j in {1, ..., n}

    Args:
       m_bold (List):                       Products of encoded selections m = (m_1, ..., m_N), m_i in G_q
       n_bold (List):                       Number of candidates n >= 2
       w_bold (List):                       Counting circles w = (w_1, ..., w_N_E), w_i \in N
       secparams (SecurityParams):          Collection of public security parameters

    Returns:
        list of int:                        Election result matrix V = (v_ij) N x n
    """

    AssertList(m_bold)
    for m in m_bold: assert IsMember(m, secparams), "m_bold elements must be in G_q"
    AssertList(n_bold)
    for n in n_bold: assert n >= 2, "n must be greater than or equal 2"
    AssertList(w_bold)
    AssertClass(secparams, SecurityParams)

    n = sum(n_bold)
    w = max(w_bold)
    N = len(m_bold)

    V_bold = []
    W_bold = []

    p_bold = GetPrimes(n+w, secparams)
    for i in range(N):
        v_bold_i = [None] * n
        for j in range(n):
            if m_bold[i] % p_bold[j] == 0:
                v_bold_i[j] = 1
            else:
                v_bold_i[j] = 0
        V_bold.append(v_bold_i)

        w_bold_i = [None] * w
        for j in range(w):
            if m_bold[i] % p_bold[n+j] == 0:
                w_bold_i[j] = 1
            else:
                w_bold_i[j] = 0
        W_bold.append(w_bold_i)

    return (V_bold, W_bold)

class GetVotesTest(unittest.TestCase):
    def testGetVotes(self):
        # Testing is done with integration tests
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
