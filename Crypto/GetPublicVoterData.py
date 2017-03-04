import gmpy2
from gmpy2 import mpz
import unittest
from SecurityContext import SECURITYCONTEXT_DEFAULT, SECURITYCONTEXT_L0, SECURITYCONTEXT_L3
from Utils import Truncate
from RecHash import RecHash

def GetPublicVoterData(x, y , ctx = SECURITYCONTEXT_DEFAULT):
    """
    Algorithm 7.11: Generates the public data for a single voter, which is sent to the bulletin board.
   
    @type   p:  list
    @param  p:  A list of points

    @rtype:     Tuple
    @return:    Public data
    """    
    h = ToInteger(RecHash(y, ctx)) % ctx.q_2
    x_2 = ctx.g_2 ** x % ctx.q_2
    y_2 = ctx.g_2 ** (y+h) % ctx.p_2

    return (x_2, y_2)

# Unit Tests
class GetPublicVoterDataTest(unittest.TestCase):

    def testOne(self):       
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()