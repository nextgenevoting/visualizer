import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils            import AssertMpz, AssertList, AssertClass, Truncate
from Crypto.SecurityParams  import SecurityParams, secparams_default, secparams_l0
from Utils.RecHash          import RecHash
from Utils.MarkByteArray    import MarkByteArray
from Utils.ToString         import ByteArrayToString
from Utils.XorByteArray     import XorByteArray


def GetReturnCodes(s, P_s, secparams=secparams_default):
    """
    Algorithm 7.28: Computes the k return codes rcs = (RC_s_1, ... , RC_s_k) for the selected
    candidates by combining the hash values of the transferred points p_ij in P_s from different authorities.

    Args:
        s (list):           Selections
        P_s (list):         Points

    Returns:
        list                Points
    """

    AssertList(s)
    AssertList(P_s)
    AssertClass(secparams, SecurityParams)

    rc_s = []
    for i in range(len(s)):
        R_j = []
        for j in range(len(P_s)):
            R_j.append(Truncate(RecHash(P_s[j][i], secparams), secparams.L_R))
        R = MarkByteArray(XorByteArray(R_j), s[i], secparams.n_max)
        rc_s.append(ByteArrayToString(R, secparams.A_R))

    return rc_s

class GetReturnCodesTest(unittest.TestCase):
    def testGetReturnCodes(self):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
