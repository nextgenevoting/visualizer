import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils           import AssertMpz, AssertList, AssertClass
from Crypto.SecurityParams import SecurityParams, secparams_default, secparams_l0
from Utils.Random          import randomMpz

def GenQuery(q, pk, secparams=secparams_default):
    """
    Algorithm 7.20: Generates an OT query a from the prime numbers representing the
    voter's selection and a for a given public encryption key (which serves as a
    generator).

    Args:
        q (list):   Selected primes
        pk (mpz):   Encryption key

    Returns:
        (a, r):     The OT query
    """

    AssertList(q)
    AssertMpz(pk)
    AssertClass(secparams, SecurityParams)

    k = len(q)
    a = [None] * k
    r = [None] * k

    for i in range(k):
        r[i] = randomMpz(secparams.q, secparams)
        a[i] = (q[i] * gmpy2.powmod(pk, r[i], secparams.p)) % secparams.p

    return (a, r)

class GenQueryTest(unittest.TestCase):
    def testGenQueryL0(self):
        pk = mpz(362)
        q = [1,3,7]         # selected primes
        (a,r) = GenQuery(q,pk, secparams_l0)
        # expected result:
        # a_i = q_i * pk^r_i mod p
        # a_i = q_i * 362^2 mod 563
        self.assertEqual(a[0], 428)  # a_0 = 1 * 131044 mod 563 = 428
        self.assertEqual(a[1], 158) # a_1 = 3 * 428 mod 563= 158
        self.assertEqual(a[2], 181) # a_2 = 7 * 428 = 181

        # Manually calculated values:
        # Selection = {1,4}, pk = 4096, p = 563
        # These values will be used to test the other oblivious transfer algorithms!
        q = [7, 17]
        (a,r) = GenQuery(q,mpz(4096), secparams_l0)
        self.assertEqual(a[0], mpz(401))
        self.assertEqual(a[1], mpz(250))

if __name__ == '__main__':
    unittest.main()
