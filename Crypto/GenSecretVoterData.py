import gmpy2
from gmpy2 import mpz
import unittest
from SecurityContext import SECURITYCONTEXT_DEFAULT, SECURITYCONTEXT_L0, SECURITYCONTEXT_L3
from Utils import Truncate, AssertList
from Crypto.Random import randomMpz
from RecHash import RecHash

def GenSecretVoterData(p, electionEvent, ctx = SECURITYCONTEXT_DEFAULT):
    """
    Algorithm 7.10: Generates the secret data for a single voter, which is sent to the voter prior to an election event via the printing authority.
   
    @type   p:  list
    @param  p:  A list of points

    @rtype:     Tuple
    @return:    Secret data
    """   
    AssertList(p)

    #todo: x und y zufällig aus q^'_x/s und q^'_y/s auswählen, aber was ist s???
    x = mpz(1)
    y = mpz(2)

    F = Truncate(RecHash(p, ctx),ctx.Lf)        # Finalization code
    r = []                                      # Return codes
    for i in range(0, electionEvent.n):
        r.append(Truncate(RecHash(p[i], ctx), ctx.Lr))  
        
    return (x,y,F,r)

# Unit Tests
class GenSecretVoterDataTest(unittest.TestCase):

    def testOne(self):       
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()