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

def CheckReturnCodes(rc, rc_prime, s):
    """
    Algorithm 7.29: Checks if every displayed return code RC'_i i matches with the return code
    RC_s_i of the selected candidate s_i as printed on the code sheet.
    Note that this algorithm is executed by humans.

    Args:
        rc (list):          Printed return codes
        rc_prime (list):    Displayed return codes rc'
        s (list):           Selections

    Returns:
        bool
    """

    AssertList(rc)
    AssertList(rc_prime)
    AssertList(s)

    for i in range(len(s)):
        if rc[s[i]] != rc_prime[i]:
            return False

    return True

class CheckReturnCodesTest(unittest.TestCase):
    def testCheckReturnCodes(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
