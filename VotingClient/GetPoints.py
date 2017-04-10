import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils           import AssertMpz, AssertList, AssertClass, Skip, Truncate
from Crypto.SecurityParams import SecurityParams, secparams_default, secparams_l0
from Types                 import *
from math                  import ceil
from Utils.RecHash         import RecHash
from Utils.ToInteger       import ToInteger
from Utils.XorByteArray    import XorByteArray

def GetPoints(beta, k, s, r, secparams=secparams_default):
    """
    Algorithm 7.26: Computes the k-by-s matrix P_s = (P_ij)k x s of the points obtained from
    the s authorities for the selection s. The points are derived from the messages included
    in the OT responses beta = (beta_1, ..., beta_s)

    Args:
        beta:               Oblivious Transfer Response
        k (list):           Number of selections
        s (list):           Selections
        r (list):           Randomizations

    Returns:
        list                Points
    """

    AssertClass(beta, Response)
    AssertList(k)
    AssertList(s)
    AssertList(r)
    AssertClass(secparams, SecurityParams)

    (b,c,d) = beta

    l_m = ceil(secparams.L_M // secparams.L)
    i = 0
    p = []

    for j in range(len(k)):
        for l in range(k[j]):
            k_l = (b[i] * gmpy2.powmod(d[j],-r[i], secparams.p)) % secparams.p
            k_tmp = bytearray()

            for l_counter in range(l_m):
                k_tmp += RecHash([k_l,l_counter], secparams)

            K_tmp = Truncate(k_tmp, secparams.L_M)
            M = XorByteArray([c[s[i]], K_tmp])
            x = ToInteger(Truncate(M,secparams.L_M//2))
            y = ToInteger(Skip(M,secparams.L_M//2))

            if x >= secparams.p_prime or y >= secparams.p_prime:
                return None

            p.append(Point(x,y))
            i += 1

    return p

class GetPointsTest(unittest.TestCase):
    def testGetPoints(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
