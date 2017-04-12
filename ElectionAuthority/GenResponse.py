import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils           import AssertMpz, AssertList, AssertClass, AssertInt, Truncate
from Crypto.SecurityParams import SecurityParams, secparams_default, secparams_l0
from Utils.Random          import randomMpz
from math                  import ceil
from Crypto.GetPrimes      import GetPrimes
from UnitTestParams        import unittestparams
from Utils.ToByteArray     import ToByteArrayN
from Utils.RecHash         import RecHash
from Types                 import *
from Utils.XorByteArray    import XorByteArray

def GenResponse(i, a_bold, pk, n_bold, K_bold, P_bold, secparams=secparams_default):
    """
    Algorithm 7.25: Generates the response beta for the given OT query a. The messages to
    transfer are byte array representations of the n points p_i = (p_i,1, ... p_i,n). Along with beta,
    the algorithm also returns the randomizations r used to generate the response.

    Args:
        i (int):         Voter Index
        a_bold (list):   Queries
        pk (mpz):        Encryption Key
        n_bold (list):   Number of candidates
        K_bold (list):   Number of selections
        P_bold (list):   Points N x n

    Returns:
        tuple:     (beta, r)
    """

    AssertInt(i)
    AssertList(a_bold)
    AssertMpz(pk)
    AssertList(n_bold)
    AssertList(K_bold)
    AssertList(P_bold)
    AssertClass(secparams, SecurityParams)

    l_M = ceil(secparams.L_M / secparams.L)
    p = GetPrimes(sum(n_bold), secparams)
    u = v = 0

    b_bold = []
    c_bold = []
    d_bold = []
    r_bold = []

    for j in range(len(n_bold)):
        r_j = randomMpz(secparams.q, secparams)
        r_bold.append(r_j)

        for l in range(K_bold[i][j]):
            b_bold.append(gmpy2.powmod(a_bold[u], r_j, secparams.p))
            u += 1

        for l in range(n_bold[j]):
            x_i_v = P_bold[i][v].x
            y_i_v = P_bold[i][v].y
            M = bytearray()
            M += ToByteArrayN(x_i_v, secparams.L_M / 2)
            M += ToByteArrayN(y_i_v, secparams.L_M / 2)
            k = gmpy2.powmod(p[v], r_j, secparams.p)
            k_tmp = bytearray()

            for l_counter in range(l_M):
                k_tmp += RecHash([k,l_counter], secparams)

            K = Truncate(k_tmp, secparams.L_M)
            c_bold.append(XorByteArray([M, K]))
            v += 1

        d_bold.append(gmpy2.powmod(pk, r_j, secparams.p))

    beta = Response(b_bold, c_bold, d_bold)

    return (beta, r_bold)

class GenResponseTest(unittest.TestCase):
    def testGenResponse(self):
        GenResponse(0, [mpz(195), mpz(401)], unittestparams.pk, unittestparams.n, unittestparams.K, unittestparams.P, secparams_l0)
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
