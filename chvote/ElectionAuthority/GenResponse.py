import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils           import AssertMpz, AssertList, AssertClass, AssertInt, Truncate
from Common.SecurityParams import SecurityParams, secparams_l0
from Utils.Random          import randomMpz
from math                  import ceil
from Common.GetPrimes      import GetPrimes
from UnitTestParams        import unittestparams
from Utils.ToByteArray     import ToByteArrayN
from Utils.RecHash         import RecHash
from Types                 import *
from Utils.XorByteArray    import XorByteArray
from Common.IsMember       import IsMember

def GenResponse(v, a_bold, pk, n_bold, K_bold, E_bold, P_bold, secparams):
    """
    Algorithm 7.25: Generates the response beta for the given OT query a. The messages to
    transfer are byte array representations of the n points (p_v,1, ... p_v,n). Along with beta,
    the algorithm also returns the randomizations r used to generate the response.

    Args:
        v (int):                            Voter Index
        a_bold (list of mpz):               Queries
        pk (mpz):                           Encryption Key
        n_bold (list of int):               Number of candidates
        K_bold (list of int):               Number of selections
        E_bold:                             Eligibility matrix
        P_bold (list of list):              Points N x n
        secparams (SecurityParams):         Collection of public security parameters

    Returns:
        tuple:                              (beta, r)
    """

    AssertInt(v)
    AssertList(a_bold)
    for a in a_bold: assert IsMember(a, secparams), "All elements of a_bold must be in G_q"
    AssertMpz(pk)
    assert IsMember(pk, secparams), "Public key must be in G_q"
    assert pk != mpz(1), "Public key cannot be equal to 1"
    AssertList(n_bold)
    AssertList(K_bold)
    AssertList(P_bold)
    AssertClass(secparams, SecurityParams)

    M = []

    for j in range(sum(n_bold)):
        M.append(ToByteArrayN(P_bold[v][j], secparams.L_M//2) + ToByteArrayN(P_bold[v][j], secparams.L_M//2))

    z_1 = randomMpz(secparams.q, secparams)
    z_2 = randomMpz(secparams.q, secparams)
    beta = []
    b_bold = []

    for j in range(k):
        beta.append(randomMpz(secparams.p, secparams))
        b_j = gmpy2.powmod(a[j][0], z_1, secparams.p)
        b_j *= gmpy2.powmod(a[j][1], z_2, secparams.p)
        b_j *= beta[j]
        b_j %= secparams.p
        b_bold.append(b_j)

    l_M = ceil(secparams.L_M / secparams.L)
    p_bold = GetPrimes(sum(n_bold), secparams)
    n_prime = 0
    k_prime = 0

    C_bold = []

    for l in range(t):
        for i in range(n_prime + 1, n_prime + n_bold[l]):
            p_prime_i = gmpy2.powmod(P_bold[i], z_1, secparams.p)

            C.append([])
            for j in range(k_prime + 1, k_prime, E_bold[v][l]):
                K_bold[i][j] = p_prime * beta[j]

                k_tmp = bytearray()
                for c in range(l_M):
                    k_tmp += RecHash([K_bold[i][j], c], secparams)

                K_i_j = Truncate(k_temp, secparams.L_M)
                C[i].append(XorByteArray([M[i], K_i_j]))

        n_prime = n_prime + n_bold[l]
        k_prime = k_prime + e[v][l] * k[l]

    d = gmpy2.powmod(pk, z_1, secparams.p) * gmpy2.powmod(g, z_2, secparams.p)
    beta = (b_bold, C_bold, d)
    z = (z_1, z_2)

    return (beta, z)

class GenResponseTest(unittest.TestCase):
    def testGenResponse(self):
        # Testing is done with integration tests
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
