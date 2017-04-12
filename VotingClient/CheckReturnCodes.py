import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils           import AssertMpz, AssertList, AssertClass, Truncate
from Crypto.SecurityParams import SecurityParams, secparams_default, secparams_l0
from Utils.RecHash         import RecHash
from Utils.MarkByteArray   import MarkByteArray
from Utils.ToString        import ByteArrayToString
from Utils.XorByteArray    import XorByteArray

def CheckReturnCodes(rc_bold, rc_prime_bold, s_bold):
    """
    Algorithm 7.29: Checks if every displayed return code RC'_i i matches with the return code
    RC_s_i of the selected candidate s_i as printed on the code sheet.
    Note that this algorithm is executed by humans.

    Args:
        rc_bold (list):          Printed return codes
        rc_prime_bold (list):    Displayed return codes rc'
        s_bold (list):           Selections

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

class CheckReturnCodesTest(unittest.TestCase):
    def testCheckReturnCodes(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
