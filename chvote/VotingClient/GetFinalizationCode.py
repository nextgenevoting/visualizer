import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Common.SecurityParams import SecurityParams, secparams_l0
from Utils.Utils           import AssertList, AssertClass, AssertInt
from Types                 import *
from Utils.XorByteArray    import XorByteArray
from Utils.ToString        import ByteArrayToString


def GetFinalizationCode(delta_bold, secparams):
    """
    Algorithm 7.38: Computes a finalization code FC by combining the values Fj received
    from the authorities.

    Args:
        delta_bold (list):                   Finalizations
        secparams (SecurityParams):          Collection of public security parameters

    Returns:
        string:                              Finalization code
    """

    AssertList(delta_bold)
    AssertClass(secparams, SecurityParams)

    F_j = [delta_bold[j][0] for j in range(len(delta_bold))]

    FC = ByteArrayToString(XorByteArray(F_j), secparams.A_F)

    return FC

class GetFinalizationCodeTest(unittest.TestCase):
    def testGetFinalizationCode(self):

        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
