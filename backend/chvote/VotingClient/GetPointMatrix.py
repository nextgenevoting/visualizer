import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils            import AssertMpz, AssertList, AssertClass
from chvote.Common.SecurityParams import SecurityParams, secparams_l0
from chvote.VotingClient.GetPoints import GetPoints
from chvote.Common.IsMember        import IsMember

def GetPointMatrix(beta_bold, s_bold, r_bold, secparams):
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
    AssertList(s_bold)
    AssertList(r_bold)
    AssertClass(secparams, SecurityParams)

    s = len(beta_bold)
    P_s_bold = [None] * s

    for i in range(s):
        P_s_bold[i] = GetPoints(beta_bold[i],s_bold,r_bold,secparams)

    # Check that the length of P_s is s x k
    for elem in P_s_bold:
        assert len(elem) == len(s_bold)

    return P_s_bold

class GetPointMatrixTest(unittest.TestCase):
    def testGetPointMatrix(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
