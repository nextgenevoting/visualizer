import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Common.SecurityParams import SecurityParams, secparams_l0
from chvote.Utils.Utils           import AssertList, AssertClass, AssertInt
from chvote.Types                 import Point
from chvote.Utils.RecHash         import RecHash
from chvote.Utils.Utils           import Truncate

def GetFinalization(v, P_bold, B, secparams):
    """
    Algorithm 7.36: Computes the finalization code F_v for voter v from the given points p_i
    and returns F_v together with the randomizations r_v used in the OT response.

    Args:
        v (int):                             Voter index
        p_bold (list of points):             Points
        B (list):                            Ballot list
        secparams (SecurityParams):          Collection of public security parameters

    Returns:
        tuple:                               delta (F_v, r_bold_v)
    """

    AssertInt(v)
    AssertList(P_bold)
    AssertList(B)
    AssertClass(secparams, SecurityParams)


    p_bold_v = P_bold[v]
    F = Truncate(RecHash(p_bold_v, secparams), secparams.L_F)

    for i in range(len(B)):
        if (B[i].voterId == v):
            z_i = B[i].randomizations

    delta = (F, z_i)
    return delta

class GetFinalizationTest(unittest.TestCase):
    def testGetFinalization(self):

        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
