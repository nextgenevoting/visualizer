import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils           import AssertList


def CheckVerificationCodes(rc_bold, rc_prime_bold, s_bold):
    """
    Algorithm 7.29: Checks if every displayed verification code RC'_i i matches with the return code
    RC_s_i of the selected candidate s_i as printed on the code sheet.
    Note that this algorithm is executed by humans.

    Args:
        rc_bold (list):                     Printed return codes
        rc_prime_bold (list):               Displayed return codes rc'
        s_bold (list):                      Selections

    Returns:
        bool
    """

    AssertList(rc_bold)
    AssertList(rc_prime_bold)
    AssertList(s_bold)

    for i in range(len(s_bold)):
        if rc_bold[s_bold[i]] != rc_prime_bold[i]:
            return False

    return True

class CheckVerificationCodesTest(unittest.TestCase):
    def testCheckVerificationCodes(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
