import gmpy2
from gmpy2 import mpz
import hashlib
import unittest
from array import array

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

    def t(self):
        """
        Returns the number of simultaneous elections, t >= 1, j \in {1, ..., t} identifies the election in an election event
        """
        return len(self.elections)

    def n(self):
        """
        Returns the total number of candidates among all elections
        """
        count = 0
        for el in self.elections:
            count += el.n_j()
        return count

    def N(self):
        """
        Returns the total number of eligible voters
        """
        return len(self.voters)

    def buildMatrix(self):
        """
        Build the eligibility matrix E = (e_ij) N x t
        """
        self.E = [[0 for j in range(self.t())] for i in range(self.N())]


        for i in range(0, len(self.voters)):
            for j in range(0, len(self.elections)):
                self.E[i][j] = True         # 1 bit indicating whether or not the voter i is eligible in election j

 

    def E(self):
        return self.E


    
class Election(object):
    candidates = []

    def __init__(self, candidates = []):
        self.candidates = candidates

    def addCandidate(self, candidate):
        self.candidates.append(candidate)

    def getCandidates(self):
        return self.candidates
    
    def n_j(self):   # numberOfCandidates
        """
        n_j >= 2 denotes the number of candidates in the j-th election of an election event
        """
        return len(self.candidates)


class Voter(object):
    description = ""
    
    def __init__(self, description):
        self.description = description

    def getDescription(self):
        return self.description
        

class Candidate(object):
    name = ""

    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name



election1 = Election([Candidate("Donald Trump"), Candidate("Hillary Clinton"), Candidate("Vladimir Putin")])
election2 = Election([Candidate("Yes"), Candidate("No"), Candidate("Empty")])
electionEvent = ElectionEvent([election1, election2], [Voter("V1"), Voter("V2"), Voter("V3"), Voter("V4"), Voter("V5")])
electionEvent.buildMatrix()

# Unit Tests
class ElectionEventTest(unittest.TestCase):
    def testOne(self):
        assertTrue(False)
      
if __name__ == '__main__':
    unittest.main()
