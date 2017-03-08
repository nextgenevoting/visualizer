import gmpy2
from gmpy2 import mpz
import unittest
from SecurityParams import secparams_l0, secparams_l1, secparams_l2, secparams_l3, secparams_def
from Utils import ToInteger, AssertInt, AssertList
from Crypto.GenPoints import GenPoints
from Crypto.GenSecretVoterData import GenSecretVoterData
from Crypto.GetPublicVoterData import GetPublicVoterData
from math import floor
import multiprocessing as mp



def GenElectorateData(parallelize, index, outQueue, n, k, E, electionEvent, secparams = secparams_def):
    """
    Algorithm 7.6: Generates the data for the whole electorate    

    @type   n:  list
    @param  n:  List with number of candidates n = (n_1, ..., n_t), n_j >= 2, n = Sigma(j=1...t) n_j

    @type   k:  list
    @type   k:  Number of selections k = (k_1, ..., k_t), 0 <= kj <= nj, kj = 0 means ineligible

    @type   E:  [int][int]
    @type   E:  Eligibility matrix [N][t]

    @rtype:     Tuple
    @return:    (d, d^, P, K)
    """
    AssertList(n)
    AssertList(k)

    d = []
    d_hat = []
    K = []      #  precomputed selection matrix Nxt
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
    
    for i in range (rangeStart, rangeEnd):  # loop over N (all voters)       
        K_i = []
        for j in range(0, electionEvent.t):
            k_ij = E[i][j] * k[j]             # if voter i is eligible to cast a vote in election j, multiply 1 * the number of selections in j
            K_i.append(k_ij)
        
        # generate n random points
        p, y = GenPoints(n, K_i, electionEvent, secparams)        
        # generate x, y values, finalization code and return codes
        x,y,F,R = GenSecretVoterData(p, electionEvent, secparams)
        
        # prepare return values
        d.append((x,y,F,R))                     # private voter data        
        d_hat.append(GetPublicVoterData(x,y,secparams)) # public voter data
        K.append(K_i)                            # precomputed selection matrix Nxt
        P.append(p)                             # points on the polynomials

    if parallelize: outQueue.put((d, d_hat, P, K))
    else: return (d, d_hat, P, K)


# Unit Tests
class GenElectorateDataTest(unittest.TestCase):

    def testOne(self):       
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()