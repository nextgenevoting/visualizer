import unittest
import os, sys
import gmpy2
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils        import AssertNumeric, AssertInt
from Utils.ToInteger    import ToInteger
from Utils.Random       import randomMpz
from SecurityParams     import secparams_default, secparams_l0, secparams_l3
from Crypto.IsMember    import IsMember

def GenPolynomial(d, secparams = secparams_default):
    """
    Algorithm 7.8: Generates the coefficients a_0,...,a_d of a random polynomial A(X) = Sigma(i=0...d) a_i X^i mod p' of degree d >= 0.
    The algorithm also accepts d = -1 as input, which we interpret as the polynomial A(X) = 0.
    In this case, the algorithm returns the coefficient list a = (0).

    Args:
       d (int):     Degree d >= -1

    Returns:
       list:        A list of coefficients a_0 ... a_d of polynomial A(X)
    """

    AssertInt(d)
    assert(d >= -1)

    a = []
    a_d = 0
    if (d == -1):
        return [0]
    else:
        for i in range (0, d):
            a.append(randomMpz(secparams.p_prime, secparams))
        # generate the last coefficient != 0
        while a_d == 0: a_d = randomMpz(secparams.p_prime, secparams)
        a.append(a_d)
    return a


def printPolynomial(a):
    """
    Helper function to print a polynomial with coefficients a

    @type   a:  list
    @param  a:  List of coefficients for polynomial P

    @rtype:     void
    @return:
    """
    print("P(x)=", end='')
    for i in range(len(a)):
        print("%dx^%d" % (a[i], i), end='')
        if i != len(a)-1: print(" + ", end='')
    print('')

# Unit Tests
class GenPolynomialTest(unittest.TestCase):

    def testOne(self):
        # check if a polynomial of degree x has x+1 coefficients
        for i in range(10):
            polynomial = GenPolynomial(i)
            print("Printing random polynomial of degree %d" %i)
            printPolynomial(polynomial)
            self.assertTrue(len(polynomial) == i+1)
            for coeff in polynomial:
                # check if each coeff. is an mpz
                self.assertTrue(coeff.__class__.__name__ == 'mpz')
if __name__ == '__main__':
    unittest.main()
