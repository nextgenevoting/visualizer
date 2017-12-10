import gmpy2
import os
import sys
import unittest
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils           import AssertMpz, AssertList, AssertClass, AssertInt, Truncate
from chvote.Common.SecurityParams import SecurityParams
from chvote.Utils.Random          import randomMpz, randomQuadResMpz
from math                  import ceil
from chvote.Common.GetPrimes      import GetPrimes
from chvote.Utils.ToByteArray     import ToByteArrayN
from chvote.Utils.RecHash         import RecHash
from chvote.Types                 import *
from chvote.Utils.XorByteArray    import XorByteArray
from chvote.Common.IsMember       import IsMember

def GenResponse(v, a_bold, pk, n_bold, k_bold, E_bold, P_bold, secparams):
    """
    Algorithm 7.25: Generates the response beta for the given OT query a. The messages to
    transfer are byte array representations of the n points (p_v,1, ... p_v,n). Along with beta,
    the algorithm also returns the randomizations r used to generate the response.

    Args:
        v (int):                            Voter Index
        a_bold (list of mpz):               Queries
        pk (mpz):                           Encryption Key
        n_bold (list of int):               Number of candidates
        k_bold (list of int):               Number of selections
        E_bold (list of list):              Eligibility matrix
        P_bold (list of list):              Points N x n
        secparams (SecurityParams):         Collection of public security parameters

    Returns:
        tuple:                              (beta, r)
    """

    AssertInt(v)
    AssertList(a_bold)
    for a in a_bold: assert IsMember(a[0], secparams), "All elements of a_bold must be in G_q"
    for a in a_bold: assert IsMember(a[1], secparams), "All elements of a_bold must be in G_q"
    AssertMpz(pk)
    assert IsMember(pk, secparams), "Public key must be in G_q"
    assert pk != mpz(1), "Public key cannot be equal to 1"
    AssertList(n_bold)
    AssertList(k_bold)
    AssertList(E_bold)
    AssertList(P_bold)
    AssertClass(secparams, SecurityParams)

    n = sum(n_bold)
    k = len(a_bold)
    t = len(n_bold)
    M = []

    z_1 = randomMpz(secparams.q, secparams)
    z_2 = randomMpz(secparams.q, secparams)

    beta = []
    b_bold = []

    for j in range(k):
        beta.append(randomQuadResMpz(secparams))
        b_j = gmpy2.powmod(a_bold[j][0], z_1, secparams.p)
        b_j *= gmpy2.powmod(a_bold[j][1], z_2, secparams.p)
        b_j *= beta[j]
        b_j %= secparams.p
        b_bold.append(b_j)

    l_M = ceil(secparams.L_M / secparams.L)
    p_bold = GetPrimes(n, secparams)

    n_prime = 0
    k_prime = 0

    C_bold = [[None for i in range(sum(k_bold))] for i in range(n)]

    for l in range(len(k_bold)):
        if E_bold[v][l] != 0:
            for i in range(n_prime, n_prime + n_bold[l]):
                p_prime_i = gmpy2.powmod(p_bold[i], z_1, secparams.p)
                M.append(ToByteArrayN(P_bold[v][i].x, secparams.L_M // 2) + ToByteArrayN(P_bold[v][i].y, secparams.L_M // 2))

                for j in range(k_prime, k_prime + E_bold[v][l] * k_bold[l]):
                    k_ij = p_prime_i * beta[j] % secparams.p
                    k_tmp = bytearray()

                    for c in range(l_M):
                        k_tmp += RecHash([k_ij,c], secparams)

                    K_ij = Truncate(k_tmp, secparams.L_M)
                    C_bold[i][j] = XorByteArray([M[i], K_ij])

            k_prime = k_prime + E_bold[v][l]* k_bold[l]
        n_prime = n_prime + n_bold[l]

    d = (gmpy2.powmod(pk, z_1, secparams.p) * gmpy2.powmod(secparams.g, z_2, secparams.p)) % secparams.p
    beta = Response(b_bold, C_bold, d)
    z = (z_1, z_2)

    return (beta, z)

class GenResponseTest(unittest.TestCase):
    def testGenResponse(self):
        # Testing is done with integration tests
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
