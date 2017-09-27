import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Common.SecurityParams import SecurityParams, secparams_l0
from Utils.Utils           import AssertList, AssertClass, AssertInt
from Types                 import Point
from Utils.RecHash         import RecHash
from Utils.Utils           import Truncate

def GetFinalization(i, P_bold, B, secparams):
    """
    Algorithm 7.37: Computes the finalization code F_i for voter i from the given points p_i
    and returns F_i together with the randomizations r_i used in the OT response.

    Args:
        i (int):                             Voter index i
        p_bold (list of points):             Points
        B (list):                            Ballot list
        secparams (SecurityParams):          Collection of public security parameters

    Returns:
        tuple:                               delta (F_i, r_bold_i)
    """

    AssertInt(i)
    AssertList(P_bold)
    AssertList(B)
    AssertClass(secparams, SecurityParams)

    r_i_bold = []
    for j in range(len(B)):
        if(B[j][0] == i):
            r_i_bold = B[j][2]

    p_bold_i = P_bold[i]
    F_i = Truncate(RecHash(p_bold_i, secparams), secparams.L_F)
    delta = (F_i, r_i_bold)

    return delta

class GetFinalizationTest(unittest.TestCase):
    def testGetFinalization(self):

        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
