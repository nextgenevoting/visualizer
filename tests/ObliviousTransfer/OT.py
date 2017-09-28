import os, sys
from gmpy2 import mpz
import gmpy2
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ObliviousTransfer.OT_utils import GetSelectedPrimes, GetPrimes, Skip, Truncate, randomMpz, randomQuadResMpz, ToByteArrayN, RecHash, XorByteArray
from math import ceil

# OT parameters
pk = 2441       # public key
g = pk          # first generator = public key
g_2 = 4         # second generator
Z_p = 2963      # order of group Z_p
Z_q = 1481      # order of group Z_q
L_M = 4         # length of message bytearray
L = 1           # hash bytelength

# Election parameters
t = 2           # number of simult. elections
k_bold = [1,1]  # number of selections per election
n_bold = [3, 3] # number of candidates

determ = True
det_z_1 = 11
det_z_2 = 22
det_beta_j = 29

def Query(s):
    k = len(s)

    # Encoding of the selection into primes
    q = GetSelectedPrimes(s, Z_p)

    a = [None] * k
    r = [None] * k
    for j in range(k):
        if not determ:
            r[j] = randomMpz(Z_q)
        else:
            r[j] = j+1
        a_j_1 = (q[j] * gmpy2.powmod(pk, r[j], Z_p)) % Z_p
        a_j_2 = gmpy2.powmod(g_2, r[j], Z_p)
        a[j] = (a_j_1, a_j_2)

    return (a, r)

def Reply(a):
    # Generate OT messages; M contains the verification codes, in this simplified example, message 1 = 0x01 0x01 0x01 0x01, message 2 = 0x02 0x02 0x02 0x02 (with L_M = 4)
    k = len(a)
    n_sum = sum(n_bold)


    M = []
    for j in range(n_sum):
        M_j = bytearray()
        M_j += ToByteArrayN(j, L_M / 2)
        M_j += ToByteArrayN(j, L_M / 2)
        M.append(M_j)

    if not determ:
        z_1 = randomMpz(Z_q)
        z_2 = randomMpz(Z_q)
    else:
        z_1 = det_z_1
        z_2 = det_z_2

    beta = [None] * k
    b = [None] * k
    for j in range(k):
        if not determ:
            beta[j] = randomQuadResMpz(Z_q, g, Z_p)
        else:
            beta[j] = det_beta_j

        b[j] = (gmpy2.powmod(a[j][0], z_1, Z_p) * gmpy2.powmod(a[j][1], z_2, Z_p) * beta[j]) % Z_p



    n_prime = k_prime = 0
    l_M = ceil(L_M / L)

    p_bold = GetPrimes(n_sum, Z_p)
    C = [[None for i in range(sum(k_bold))] for i in range(n_sum)]

    for l in range(t):
        for i in range(n_prime, n_prime + n_bold[l]):
            p_prime_i = gmpy2.powmod(p_bold[i], z_1, Z_p)

            for j in range(k_prime, k_prime + k_bold[l]):
                k_ij = p_prime_i * beta[j]
                k_tmp = bytearray()

                for c in range(l_M):
                    k_tmp += RecHash([k_ij, c], L)

                K_ij = Truncate(k_tmp, L_M)
                C[i][j] = XorByteArray([M[i], K_ij])

        n_prime = n_prime + n_bold[l]
        k_prime = k_prime + k_bold[l]

    d = (gmpy2.powmod(pk, z_1, Z_p) * gmpy2.powmod(g_2, z_2, Z_p)) % Z_p
    beta = (b, C, d)
    z = (z_1, z_2)
    return (beta, z)


def Open(beta, s, r):
    (b, C_bold, d) = beta

    k = len(s)

    l_M = ceil(L_M // L)

    M = []
    for j in range(k):
        k_j = (b[j] * gmpy2.powmod(d, -r[j], Z_p)) % Z_p

        K = bytearray()
        for c in range(l_M):
            K += RecHash([k_j, c], L)

        K_j = Truncate(K, L_M)
        M_j = XorByteArray([C_bold[s[j]][j], K_j])
        M.append(M_j)

    return M

if __name__ == '__main__':
    s = [0,2]
    (a, r) = Query(s)
    (beta, z) = Reply(a)
    M = Open(beta, s, r)

    for m in M:
        print(m)

