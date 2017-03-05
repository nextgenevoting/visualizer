import gmpy2
from gmpy2 import mpz
import unittest
from SecurityContext import SECURITYCONTEXT_DEFAULT, SECURITYCONTEXT_L0, SECURITYCONTEXT_L3
from Utils import ToInteger, AssertInt
from Crypto.GenPoints import GenPoints
from Crypto.GenSecretVoterData import GenSecretVoterData
from Crypto.GetPublicVoterData import GetPublicVoterData

def GenElectorateData(n,k,E, electionEvent, ctx = SECURITYCONTEXT_DEFAULT):
    """
    Algorithm 7.6: Generates the data for the whole electorate    

    @type   n:  int
    @param  n:  Number of candidates n = (n_1, ..., n_t), n_j >= 2, n = Sigma(j=1...t) n_j

    @type   k:  int
    @type   k:  Number of selections k = (k_1, ..., k_t), 0 <= k_j <= n_j # k_j = 0 means ineligible

    @type   E:  matrix
    @type   E:  Eligibility matrix

    @rtype:     Tuple
    @return:    (d,d^, P, K)
    """  
    d = []
    d_2 = []  
    K = []
    P = []
    for i in range (0, electionEvent.N):
        eligibilityCount = 0
        Ktemp = []
        for j in range(0, electionEvent.t):
            eligibilityCount += E[i][j]
            Ktemp.append(E[i][j])
        p, y = GenPoints(n, eligibilityCount, electionEvent, ctx)
        x,y,F, R = GenSecretVoterData(p, electionEvent, ctx)
        d.append((x,y,F,R))
        
        d_2.append(GetPublicVoterData(x,y,ctx))
        K.append(Ktemp)
        P.append(p)

    return (d, d_2, P, K)   



# Unit Tests
class GenElectorateDataTest(unittest.TestCase):

    def testOne(self):       
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()