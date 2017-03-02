import gmpy2
from gmpy2 import mpz
from SecurityContext import SECURITYCONTEXT_DEFAULT, SECURITYCONTEXT_L0, SECURITYCONTEXT_L3
from Random import randomMpz
import unittest
from Utils import Truncate
from GetYValue import GetYValue
from RecHash import RecHash
from ElectionEvent import electionEvent

def GenSecretVoterData(p, ctx = SECURITYCONTEXT_DEFAULT, elEvent = electionEvent):
    """
    Algorithm 7.10: Generates the secret data for a single voter, which is sent to the voter prior to an election event via the printing authority.
   
    @type   p:  list
    @param  p:  A list of points

    @rtype:     Tuple
    @return:    Secret data
    """    
    #todo: x und y zufällig aus q^'_x/s und q^'_y/s auswählen, aber was ist s???
    x = 1
    y = 2

    LF = 3  #todo : The length of the finalization code LF must be calulated depending on the deterrence factor etc.. The calculation is described on page 40
    LR = 2  #todo : The length of the return codes LR must be calulated depending on the deterrence factor etc.. The calculation is described on page 40

    F = Truncate(RecHash(p, ctx),LF)            # Finalization code
    r = []                                      # Return codes
    for i in range(0, elEvent.n):
        r.append(Truncate(RecHash(p[i], ctx), LR))
    
        
    return (x,y,F,r)

# Unit Tests
class GenSecretVoterDataTest(unittest.TestCase):

    def testOne(self):       
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()