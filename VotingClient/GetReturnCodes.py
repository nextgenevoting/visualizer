import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils           import AssertMpz, AssertList, AssertClass, Truncate
from Crypto.SecurityParams import SecurityParams
from Utils.RecHash         import RecHash
from Utils.MarkByteArray   import MarkByteArray
from Utils.ToString        import ByteArrayToString
from Utils.XorByteArray    import XorByteArray

def GetReturnCodes(s_bold, P_s_bold, secparams):
    """
    Algorithm 7.28: Computes the k return codes rcs = (RC_s_1, ... , RC_s_k) for the selected
    candidates by combining the hash values of the transferred points p_ij in P_s from different authorities.

    Args:
        s_bold (list):           Selections
        P_s_bold (list):         Points

    Returns:
        list                Points
    """

    AssertList(s_bold)
    AssertList(P_s_bold)
    AssertClass(secparams, SecurityParams)

    rc_s_bold = []

    for i in range(len(s_bold)):
        R_j = []

        for j in range(len(P_s_bold)):
            R_j.append(Truncate(RecHash(P_s_bold[j][i], secparams), secparams.L_R))

        R = MarkByteArray(XorByteArray(R_j), s_bold[i], secparams.n_max)
        rc_s_bold.append(ByteArrayToString(R, secparams.A_R))

    return rc_s_bold

class GetReturnCodesTest(unittest.TestCase):
    def testGetReturnCodes(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
