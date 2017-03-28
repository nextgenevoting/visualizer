import unittest
import os, sys
import gmpy2
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                        import AssertNumeric, AssertList, AssertMpz, AssertClass
from Crypto.SecurityParams              import SecurityParams, secparams_default, secparams_l0, secparams_l3

def GetYValue(x, a, secparams = secparams_default):
    """
    Algorithm 7.9: Computes the value y = A(x) ∈ Z_p' obtained from evaluating the polynomial A(X) = Sigma(i=0...d) a_i X^i mod p' at position x.
    The algorithm is an implementation of Horners method.

    Args:
       x (mpz):     value x \in Z_p', normally mpz is used except for x = 0
       a (list):    list of coefficients

    Returns:
       mpz:         the y value for x on the polynomial
    """
    AssertMpz(x)
    AssertList(a)
    AssertClass(secparams, SecurityParams)

    if x == mpz(0):
        y = mpz(a[0])
    else:
        y = mpz(0)
        for i in reversed(range(len(a))):
            y = (a[i] + x * y) % secparams.p_prime

    AssertMpz(y)
    return y

# Unit Tests
class GetYValueTest(unittest.TestCase):

    def testGetYValueL0(self):
        # Test 1: Compare with manually calculated value
        a = [1,3,6,9,15]    # P(x) = 1 + 3x + 6x^2 + 9x^3 + 15x^4
        #solved with wolfram alpha: P(17) = y = (1+3*17 +6*17^2+9*17^3+15*17^4 )% 131 = 84
        self.assertTrue(GetYValue(mpz(17), a, secparams_l0) == 84)

if __name__ == '__main__':
    unittest.main()
