import unittest
import os, sys
import gmpy2
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils           import AssertInt, AssertClass
from chvote.Utils.Random          import randomMpz
from chvote.Common.SecurityParams import SecurityParams, secparams_l0, secparams_l3

def GenPolynomial(d, secparams):
    """
    Algorithm 7.8: Generates the coefficients a_0,...,a_d of a random polynomial A(X) = Sigma(i=0...d) a_i X^i mod p' of degree d >= 0.
    The algorithm also accepts d = -1 as input, which we interpret as the polynomial A(X) = 0.
    In this case, the algorithm returns the coefficient list a = (0).

    Args:
       d (int):                            Degree d >= -1
       secparams (SecurityParams):         Collection of public security parameters

    Returns:
       list of mpz:                        A list of coefficients a_0 ... a_d of polynomial A(X)
    """

    AssertInt(d)
    AssertClass(secparams, SecurityParams)
    assert(d >= -1)

    a_bold = []
    a_d = 0

    if (d == -1):
        return [0]

    else:
        for i in range (d):
            a_bold.append(randomMpz(secparams.p_prime, secparams))

        # generate the last coefficient != 0
        while a_d == 0:
            a_d = randomMpz(secparams.p_prime, secparams)

        a_bold.append(a_d)

    return a_bold

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
        if i != len(a) - 1:
            print(" + ", end='')

    print()

class GenPolynomialTest(unittest.TestCase):
    def testGenPolynomial(self):
        # check if a polynomial of degree x has x+1 coefficients
        for i in range(10):
            print("Printing random polynomial of degree %d" % i)

            polynomial = GenPolynomial(i,secparams_l3)
            printPolynomial(polynomial)
            self.assertTrue(len(polynomial) == i+1)

            for coeff in polynomial:
                # check if each coeff. is an mpz
                self.assertTrue(coeff.__class__.__name__ == 'mpz')

if __name__ == '__main__':
    unittest.main()
