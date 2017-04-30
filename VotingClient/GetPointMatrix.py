import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils            import AssertMpz, AssertList, AssertClass
from Crypto.SecurityParams  import SecurityParams, secparams_l0
from VotingClient.GetPoints import GetPoints
from Crypto.IsMember        import IsMember

def GetPointMatrix(beta_bold, k_bold, s_bold, r_bold, secparams):
    """
    Algorithm 7.26: Computes the k-by-s matrix P_s = (P_ij)k x s of the points obtained from
    the s authorities for the selection s. The points are derived from the messages included
    in the OT responses beta = (beta_1, ..., beta_s)

    Args:
        beta_bold (list of Response):       Oblivious Transfer Responses
        k_bold (list of int):               Number of selections
        s_bold (list of int):               Selections
        r_bold (list of mpz):               Randomizations
        secparams (SecurityParams):         Collection of public security parameters

    Returns:
        list                                Points
    """

    AssertList(beta_bold)
    AssertList(k_bold)
    AssertList(s_bold)
    AssertList(r_bold)
    AssertClass(secparams, SecurityParams)

    s = len(beta_bold)
    P_s_bold = [None] * s

    for j in range(s):
        P_s_bold[j] = GetPoints(beta_bold[j],k_bold,s_bold,r_bold,secparams)

    return P_s_bold

class GetPointMatrixTest(unittest.TestCase):
    def testGetPointMatrix(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
