import unittest
import os, sys
import gmpy2
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                        import AssertNumeric, AssertList, AssertMpz
from Utils.ToInteger                    import ToInteger
from Crypto.SecurityParams              import secparams_default, secparams_l0, secparams_l3
from Crypto.IsMember                    import IsMember
from Utils.Random                       import randomMpz
from ElectionAuthority.GenPolynomial    import GenPolynomial, printPolynomial

def GetYValue(x, a, secparams = secparams_default):
    """
    Algorithm 7.9: Computes the value y = A(x) in Z_p' obtained from evaluating the polynomial A(X) = Sigma(i=0...d) a_i X^i mod p' at position x.
    The algorithm is an implementation of Horners method.

    Args:
       x (mpz):     value x \in Z_p', normally mpz is used except for x = 0
       a (list):    list of coefficients

    Returns:
       mpz:         the y value for x on the polynomial
    """
    AssertNumeric(x)
    AssertList(a)
    assert(x.__class__.__name__ == 'mpz' and x > 0 or isinstance(x, int) and x == 0)    # check that x is only of type int if it's value is 0 (otherwise it must be mpz!)

    if x == 0:
        y = a[0]
    else:
        y = 0
        for i in reversed(range(len(a))):
            y = (a[i] + x * y) % secparams.p_prime

    AssertMpz(y)
    return y

# Unit Tests
class GetYValueTest(unittest.TestCase):

    def testOne(self):
        # Test 1: Compare with manually calculated value
        a = [1,3,6,9,15]    # P(x) = 1 + 3x + 6x^2 + 9x^3 + 15x^4
        #solved with wolfram alpha: P(17) = y = (1+3*17 +6*17^2+9*17^3+15*17^4 )% 131 = 84
        self.assertTrue(GetYValue(mpz(17), a, secparams_l0) == 84)

if __name__ == '__main__':
    unittest.main()
