import gmpy2
from gmpy2 import mpz
import hashlib
import unittest
from array import array
from Candidate import Candidate
from Voter import Voter
from Election import Election

class ElectionEvent(object):
    """
    This class holds all parameters relevant to an election event.
    """

    elections = []
    voter = []
    E = []               # eligibility matrix E = (e_ij) N x t

    def __init__(self, elections = [], voters = []):
        self.elections = elections
        self.voters = voters
        self.buildEligibilityMatrix()

    @property
    def t(self):
        """
        Returns the number of simultaneous elections, t >= 1, j \in {1, ..., t} identifies the election in an election event

        Returns:
           int     the number of simultaneous elections
        """
        return len(self.elections)

    @property
    def n(self):
        """
        Returns the number of candidates n  (n1,...,nt) n_j >= 2

        Returns:
           list:  A list of length t with the number of candidates per election
        """
        n = []
        for election in self.elections:
            n.append(election.n)
        return n

    @property
    def n_total(self):
        """
        Returns the total number of candidates among all elections

        Returns:
           int:  The total number of candidates
        """
        count = 0;
        for n_i in self.n:
            count += n_i
        return count

    @property
    def N(self):
        """
        Returns the total number of eligible voters

        Returns:
           int:     the total number of eligible voters
        """
        return len(self.voters)

    def buildEligibilityMatrix(self):
        """
        Build the eligibility matrix E = (e_ij) N x t

        """
        self.E = [[0 for j in range(self.t)] for i in range(self.N)]

        for i in range(0, len(self.voters)):
            for j in range(0, len(self.elections)):
                self.E[i][j] = True         # 1 bit indicating whether or not the voter i is eligible in election j


    def E(self):
        """
        Returns the eligibility matrix E = (e_ij) N x t

        returns:
            [int][int] Eligibility matrix E = (e_ij) N x t
        """
        return self.E


dummyElectionEvent = ElectionEvent([Election([Candidate("Donald Trump"), Candidate("Hillary Clinton"), Candidate("Vladimir Putin")]), Election([Candidate("Yes"), Candidate("No"), Candidate("Empty")])], [Voter("V1"), Voter("V2"), Voter("V3")])

# Unit Tests
class ElectionEventTest(unittest.TestCase):
    def testOne(self):
        assertTrue(False)

if __name__ == '__main__':
    unittest.main()

