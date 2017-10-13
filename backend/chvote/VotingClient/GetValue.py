import gmpy2
import os
import sys
import unittest
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Common.SecurityParams import SecurityParams, secparams_l0
from chvote.Utils.Utils           import AssertList, AssertClass
from chvote.Types                 import Point

def GetValue(p_bold, secparams):
    """
    Algorithm 7.32: Computes a polynomial A(X) of degree k - 1 from given
    points p = (p_1, ..., p_k) using Lagrange's interpolation method and returns
    the value y = A(0).

    Args:
        p_bold (list of points):             Given points
        secparams (SecurityParams):          Collection of public security parameters

    Returns:
        y: y = A(0) of polynomial A(X)
    """

    AssertList(p_bold)
    AssertClass(secparams, SecurityParams)

    y = 0
    k = len(p_bold)

    for i in range(k):
        n = mpz(1)
        d = mpz(1)

        for j in range(k):
            if i != j:
                n = (n * p_bold[j].x) % secparams.p_prime
                d = (d * (p_bold[j].x - p_bold[i].x)) % secparams.p_prime

        y = (y + p_bold[i].y * n * gmpy2.invert(d, secparams.p_prime)) % secparams.p_prime

    return y

class GetValueTest(unittest.TestCase):
    def testGetValue(self):
        p = [ Point(1, 3)
            , Point(4, 7)
            , Point(8, 5)
            ]

        print(GetValue(p, secparams_l0))

        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
