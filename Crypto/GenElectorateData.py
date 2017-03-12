import unittest
import os, sys
import gmpy2
from gmpy2 import mpz
from math import floor
import multiprocessing as mp

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                import AssertInt, AssertList
from Utils.ToInteger            import ToInteger
from SecurityParams             import secparams_l0, secparams_l1, secparams_l2, secparams_l3, secparams_default
from Crypto.GenPoints           import GenPoints
from Crypto.GenSecretVoterData  import GenSecretVoterData
from Crypto.GetPublicVoterData  import GetPublicVoterData
from Voter                      import Voter
from ElectionEvent              import ElectionEvent
from Election                   import Election
from Candidate                  import Candidate

def GenElectorateData(parallelize, index, outQueue, n, k, E, N,t, secparams = secparams_default):
    """
    Algorithm 7.6: Generates the data for the whole electorate

    Args:
        n (list):     A list containing the number of candidates: (n_1, ... , n_t)
        k (list):     A list containing the number of possible selections per election: (k_1, ... , k_t)
        E ([int][int]):       Eligibility matrix [N][t], 1 means eligible

    Returns:
        tuple:       (d, d^, P, K)
    """
    AssertList(n)
    AssertList(k)

    d = []
    d_hat = []
    K = []      #  precomputed selection matrix Nxt
    P = []

    rangeStart = 0
    rangeEnd = N
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
        for j in range(0, t):
            k_ij = E[i][j] * k[j]             # if voter i is eligible to cast a vote in election j, multiply 1 * the number of selections in j
            K_i.append(k_ij)

        # generate n random points
        p, y = GenPoints(n, K_i, t, secparams)
        # generate x, y values, finalization code and return codes
        x,y,F,R = GenSecretVoterData(p, secparams)

        # prepare return values
        d.append((x,y,F,R))                     # private voter data
        d_hat.append(GetPublicVoterData(x,y, p, secparams)) # public voter data
        K.append(K_i)                           # precomputed selection matrix Nxt
        P.append(p)                             # points on the polynomials

    if parallelize: outQueue.put((d, d_hat, P, K))
    else: return (d, d_hat, P, K)


# Unit Tests
class GenElectorateDataTest(unittest.TestCase):

    def testGenElectorateData(self):
        voters = []
        votersCount = 10
        for i in range (votersCount):
            voters.append(Voter("Voter"+str(i)))

        electionEvent = ElectionEvent([Election([Candidate("Donald Trump"), Candidate("Hillary Clinton"), Candidate("Vladimir Putin")]), Election([Candidate("Yes"), Candidate("No"), Candidate("Empty")])], voters)

        d, d_hat, P, K = GenElectorateData(False, None, None, electionEvent.n, [1,1], electionEvent.E, electionEvent.N, electionEvent.t)

        # Test if len(d) matches the number of voters
        self.assertTrue(len(d) == votersCount)

        # Check the secret voter data
        # The elements of d must be tuples with 4 values
        for di in d:
            self.assertTrue(len(di) == 4 and di[0].__class__.__name__ == 'mpz' and di[1].__class__.__name__ == 'mpz' and isinstance(di[2], bytes) and isinstance(di[3], list))
            self.assertTrue(len(di[3]) == electionEvent.n_total)


if __name__ == '__main__':
    unittest.main()
