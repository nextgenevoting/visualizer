import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils            import AssertMpz
from Crypto.SecurityParams  import secparams_default
from Crypto.Random          import randomMpz

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

    AssertMpz(pk)

    k = len(q)
    a = [None] * k
    r = [None] * k

    for i in range(k):
        r[i] = randomMpz(secparams.q, secparams)
        a[i] = q[i] * gmpy2.powmod(pk, r[i], secparams.p)

    return (a, r)

class GenQueryTest(unittest.TestCase):
    def testGenQuery(self):
        self.assertTrue(False) # TODO

if __name__ == '__main__':
    unittest.main()
