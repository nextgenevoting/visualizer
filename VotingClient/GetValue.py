import unittest
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Crypto.SecurityParams import SecurityParams, secparams_default, secparams_l0
from Utils.Utils           import AssertList, AssertClass
from Types                 import Point

def GetValue(p_bold, secparams=secparams_default):
    """
    Algorithm 7.32: Computes a polynomial A(X) of degree k - 1 from given
    points p = (p_1, ..., p_k) using Lagrange's interpolation method and returns
    the value y = A(0).

    Args:
        p_bold (list of points): Given points

    Returns:
        y: y = A(0) of polynomial A(X)
    """

    AssertList(p_bold)
    AssertClass(secparams, SecurityParams)

    y = 0
    k = len(p_bold)

    for i in range(k):
        n = 1
        d = 1

        for j in range(k):
            if i != j:
                n = (n * p_bold[j].x) % secparams.p_prime
                d = (d * (p_bold[j].x - p_bold[i].x)) % secparams.p_prime

        y = (y + p_bold[i].y * n // d) % secparams.p_prime

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
