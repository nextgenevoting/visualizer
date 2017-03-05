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

    def addElection(self, election):
        self.elections.append(election)

    @property
    def t(self):
        """
        Returns the number of simultaneous elections, t >= 1, j \in {1, ..., t} identifies the election in an election event
        """
        return len(self.elections)
        
    @property
    def n(self):
        """
        Returns the total number of candidates among all elections
        """
        count = 0
        for el in self.elections:
            count += el.n
        return count

    @property
    def N(self):
        """
        Returns the total number of eligible voters
        """
        return len(self.voters)

    def buildMatrix(self):
        """
        Build the eligibility matrix E = (e_ij) N x t
        """
        self.E = [[0 for j in range(self.t)] for i in range(self.N)]


        for i in range(0, len(self.voters)):
            for j in range(0, len(self.elections)):
                self.E[i][j] = True         # 1 bit indicating whether or not the voter i is eligible in election j

 

    def E(self):
        return self.E

# Unit Tests
class ElectionEventTest(unittest.TestCase):
    def testOne(self):
        assertTrue(False)
      
if __name__ == '__main__':
    unittest.main()

