import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils           import AssertMpz, AssertList, AssertClass, Skip, Truncate
from Crypto.SecurityParams import SecurityParams, secparams_l0
from Types                 import *
from math                  import ceil
from Utils.RecHash         import RecHash
from Utils.ToInteger       import ToInteger
from Utils.XorByteArray    import XorByteArray

def GetPoints(beta, k_bold, s_bold, r_bold, secparams):
    """
    Algorithm 7.26: Computes the k-by-s matrix P_s = (P_ij)k x s of the points obtained from
    the s authorities for the selection s. The points are derived from the messages included
    in the OT responses beta = (beta_1, ..., beta_s)

    Args:
        beta (Response):                     Oblivious Transfer Response
        k_bold (list of int):                Number of selections
        s_bold (list of int):                Selections
        r_bold (list of mpz):                Randomizations
        secparams (SecurityParams):          Collection of public security parameters

    Returns:
        list                                 Points
    """

    AssertClass(beta, Response)
    AssertList(k_bold)
    AssertList(s_bold)
    AssertList(r_bold)
    AssertClass(secparams, SecurityParams)

    (b,c,d) = beta

    l_m = ceil(secparams.L_M // secparams.L)
    i = 0
    p_bold = []

    for j in range(len(k_bold)):
        for l in range(k_bold[j]):
            k = (b[i] * gmpy2.powmod(d[j],-r_bold[i], secparams.p)) % secparams.p

            K = bytearray()
            for l_counter in range(l_m):
                K += RecHash([k,l_counter], secparams)

            K = Truncate(K, secparams.L_M)
            M = XorByteArray([c[s_bold[i]], K])
            x = ToInteger(Truncate(M,secparams.L_M//2))
            y = ToInteger(Skip(M,secparams.L_M//2))

            if x >= secparams.p_prime or y >= secparams.p_prime:
                return None

            p_bold.append(Point(x,y))
            i += 1

    return p_bold

class GetPointsTest(unittest.TestCase):
    def testGetPoints(self):
        # Testing is done with integration tests
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
