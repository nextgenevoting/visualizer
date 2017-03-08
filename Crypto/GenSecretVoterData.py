import gmpy2
from gmpy2 import mpz
import unittest
from SecurityParams import secparams_def, secparams_l0, secparams_l3
from Utils import Truncate, AssertList
from Crypto.Random import randomMpz
from RecHash import RecHash
from math import floor

def GenSecretVoterData(p, electionEvent, secparams = secparams_def):
    """
    Algorithm 7.10: Generates the secret data for a single voter, which is sent to the voter prior to an election event via the printing authority.
   
    @type   p:  list
    @param  p:  A list of points

    @rtype:     Tuple
    @return:    Secret data
    """   
    AssertList(p)

    q_hat_apos_x = floor(secparams.q_hat_X // secparams.s)
    q_hat_apos_y = floor(secparams.q_hat_Y // secparams.s)
    x = randomMpz(q_hat_apos_x)
    y = randomMpz(q_hat_apos_y)

    F = Truncate(RecHash(p, secparams),secparams.L_F)        # Finalization code
    r = []                                      # Return codes
    for i in range(0, len(p)):
        r.append(Truncate(RecHash(p[i], secparams), secparams.L_R))  
        
    return (x,y,F,r)

# Unit Tests
class GenSecretVoterDataTest(unittest.TestCase):

    def testOne(self):       
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()