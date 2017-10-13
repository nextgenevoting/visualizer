import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils           import AssertMpz, AssertList, AssertClass, Skip, Truncate
from chvote.Common.SecurityParams import SecurityParams, secparams_l0
from chvote.Types                 import *
from math                  import ceil
from chvote.Utils.RecHash         import RecHash
from chvote.Utils.ToInteger       import ToInteger
from chvote.Utils.XorByteArray    import XorByteArray

def GetPoints(beta, s_bold, r_bold, secparams):
    """
    Algorithm 7.26: Computes the k-by-s matrix P_s = (P_ij)k x s of the points obtained from
    the s authorities for the selection s. The points are derived from the messages included
    in the OT responses beta = (beta_1, ..., beta_s)

    Args:
        beta (Response):                     Oblivious Transfer Response
        s_bold (list of int):                Selections
        r_bold (list of mpz):                Randomizations
        secparams (SecurityParams):          Collection of public security parameters

    Returns:
        list                                 Points
    """

    AssertClass(beta, Response)
    AssertList(s_bold)
    AssertList(r_bold)
    AssertClass(secparams, SecurityParams)

    (b_bold,C_bold,d) = beta

    k = len(s_bold)

    l_M = ceil(secparams.L_M // secparams.L)

    p_bold = []

    for j in range(k):
        k_j = (b_bold[j] * gmpy2.powmod(d, -r_bold[j], secparams.p)) % secparams.p

        K_j = bytearray()
        for c in range(l_M):
            K_j += RecHash([k_j,c], secparams)

        K_j = Truncate(K_j, secparams.L_M)
        M_j = XorByteArray([C_bold[s_bold[j]][j], K_j])
        x_j = ToInteger(Truncate(M_j,secparams.L_M//2))
        y_j = ToInteger(Skip(M_j,secparams.L_M//2))

        if x_j >= secparams.p_prime or y_j >= secparams.p_prime:
            return None

        p_bold.append(Point(x_j,y_j))

    return p_bold

class GetPointsTest(unittest.TestCase):
    def testGetPoints(self):
        # Testing is done with integration tests
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
