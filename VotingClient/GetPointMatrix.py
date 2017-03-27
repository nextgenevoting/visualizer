import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils            import AssertMpz, AssertList, AssertClass
from Crypto.SecurityParams  import SecurityParams, secparams_default, secparams_l0
from VotingClient.GetPoints import GetPoints

def GetPointMatrix(beta, k, s, r, secparams=secparams_default):
    """
    Algorithm 7.26: Computes the k-by-s matrix P_s = (P_ij)k x s of the points obtained from
    the s authorities for the selection s. The points are derived from the messages included
    in the OT responses beta = (beta_1, ..., beta_s)

    Args:
        beta (list):        Oblivious Transfer Responses
        k (list):           Number of selections
        s (list):           Selections
        r (list):           Randomizations

    Returns:
        list                Points
    """

    AssertList(beta)
    AssertList(k)
    AssertList(s)
    AssertList(r)
    AssertClass(secparams, SecurityParams)

    P_s = []
    for j in range(len(beta)):
        P_s.append(GetPoints(beta,k,s,r,secparams))

    return P_s

class GetPointMatrixTest(unittest.TestCase):
    def testGetPointMatrix(self):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
