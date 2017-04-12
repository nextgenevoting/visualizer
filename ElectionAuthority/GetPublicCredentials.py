import unittest
import os, sys
import gmpy2
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils           import AssertClass, AssertList
from Crypto.SecurityParams import SecurityParams, secparams_default, secparams_l0, secparams_l3

def GetPublicCredentials(D_hat_bold, secparams = secparams_default):
    """
    Algorithm 7.12: Computes lists x^ and y^ of public voter credentials, which are obtained by
    multiplying corresponding values from the public parts of electorate data generated by the authorities.

    Args:
       D_hat (list):      Contains s public voter parameter entries (d_hat_j)

    Returns:
       tuple:    (x_hat, y_hat), Public data
    """

    AssertList(D_hat_bold)
    AssertClass(secparams, SecurityParams)
    assert len(D_hat_bold) == secparams.s, "The length of D_hat must match the number of authorities s"

    N_E = len(D_hat_bold[0])

    x_hat_bold = []
    y_hat_bold = []

    for i in range (N_E):  # loop over N (voters)
        x_hat_i = mpz(1)
        y_hat_i = mpz(1)

        for j in range(secparams_default.s):    # loop over s (authorities)
            x_hat_i = (x_hat_i * D_hat_bold[j][i][0]) % secparams.p_hat           # multiply all x values
            y_hat_i = (y_hat_i * D_hat_bold[j][i][1]) % secparams.p_hat           # multiply all y values

        x_hat_bold.append(x_hat_i)
        y_hat_bold.append(y_hat_i)

    return (x_hat_bold, y_hat_bold)

class GetPublicCredentialsTest(unittest.TestCase):
    def testGetPublicCredentialsL0(self):
        # 3 shares of 2 voter credentials, 1st value is the x-credential, 2nd value is the y-credential
        D_hat = [
            [(mpz(161), mpz(253)), (mpz(161), mpz(253))],
            [(mpz(161), mpz(253)), (mpz(161), mpz(253))],
            [(mpz(161), mpz(253)), (mpz(161), mpz(253))]
        ]
        (x_hat, y_hat) = GetPublicCredentials(D_hat,secparams_l0)
        self.assertEqual(x_hat[0], 607)         # x_hat = 161^3 mod 787 = 607
        self.assertEqual(x_hat[1], 607)         # x_hat = 161^3 mod 787 = 607
        self.assertEqual(y_hat[0], 178)         # y_hat = 253^3 mod 787 = 178
        self.assertEqual(y_hat[1], 178)         # y_hat = 253^3 mod 787 = 178

if __name__ == '__main__':
    unittest.main()
