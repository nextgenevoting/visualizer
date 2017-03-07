import gmpy2
from gmpy2 import mpz
import unittest
from SecurityContext import SECURITYCONTEXT_DEFAULT, SECURITYCONTEXT_L0, SECURITYCONTEXT_L3
from Utils import ToInteger, AssertInt
from Crypto.GenPoints import GenPoints
from Crypto.GenSecretVoterData import GenSecretVoterData
from Crypto.GetPublicVoterData import GetPublicVoterData
from math import floor
import multiprocessing as mp



def GenElectorateData(parallelize, index, outQueue, n, k,E, electionEvent, ctx = SECURITYCONTEXT_DEFAULT):
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
    
    rangeStart = 0
    rangeEnd = electionEvent.N
    if parallelize:
        # partitioning for multiprocessing (example: 4 processes, 40003 voter. p1 generates for 0-9999, p2 for 10000-19999, p3 for 20000-29999, p4: 30000-40003)
        cpuCount =  mp.cpu_count()
        partSize = electionEvent.N // cpuCount
        rangeStart = index * partSize    
 
        if (electionEvent.N % cpuCount) != 0 and index == cpuCount-1:        
            partSize = partSize + electionEvent.N % cpuCount
        rangeEnd = rangeStart + partSize    
    
    for i in range (rangeStart, rangeEnd):
        eligibilityCount = 0
        Ktemp = []
        for j in range(0, electionEvent.t):
            eligibilityCount += E[i][j]
            Ktemp.append(E[i][j])
        
        # generate n random points
        p, y = GenPoints(n, eligibilityCount, electionEvent, ctx)        
        # generate x, y values, finalization code and return codes
        x,y,F,R = GenSecretVoterData(p, electionEvent, ctx)
        
        # prepare return values
        d.append((x,y,F,R))                     # private voter data        
        d_2.append(GetPublicVoterData(x,y,ctx)) # public voter data
        K.append(Ktemp)                         # precalculated: eligibility for voter
        P.append(p)

    if parallelize: outQueue.put((d, d_2, P, K))
    else: return (d, d_2, P, K)


# Unit Tests
class GenElectorateDataTest(unittest.TestCase):

    def testOne(self):       
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()