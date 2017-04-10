import unittest
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Crypto.SecurityParams import SecurityParams, secparams_default, secparams_l0
from Utils.Utils           import AssertList, AssertClass
from VotingClient.GetValue import GetValue
from Types                 import Point

def GetValues(p, k, secparams=secparams_default):
    """
    Algorithm 7.31: Computes the values y_j = A_j(0) of the t polynomials
    A_j(X) of degree k_j - 1 interpolated from k = Sum^t_j=1 k_j points p = (p_1,
    ..., p_k).

    Args:
        p (list of points): Given points
        k (list): Number of selections

    Returns:
        y: Computed values A_j(0) of the t polynomials A_j(X)
    """

    AssertList(p)
    AssertList(k)
    AssertClass(secparams, SecurityParams)

    i = 0
    t = len(k)
    y = [None] * t

    for j in range(t):
        p_j = p[i:i+k[j]-1]
        y[j] = GetValue(p_j, secparams)
        i = i + k[j]

    return y

class GetValuesTest(unittest.TestCase):
    def testGetValues(self):
        p = [ Point(1, 3)
            , Point(4, 7)
            , Point(8, 5)
            ]
        k = [1, 2, 3]

        print(GetValues(p, k))

        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
