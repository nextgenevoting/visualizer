import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils            import AssertMpz
from Crypto.SecurityParams  import secparams_default
from Utils.Random           import randomMpz
from TestParams             import testparams

def GetVotingPage(i, c, n, k):
    """
    Algorithm 7.17: Computes a string P in A_UCS^*, which represents the voting page displayed
    to voter. Specifying the details of presenting the information on the voting page is beyond
    the scope of this document.

    Args:
        i (int):    Voter index i ∈ N
        c (list):   Candidate descriptions c = (C_1, ..., C_n), c_i ∈ A_UCS^*
        n (list):   Number of candidates n =(n_1, ..., n_t), n_j >= 2
        k (list):   Number of selections k = (k_1, ..., k_t), 0 <= k_j < n_j

    Returns:
        string:     String P ∈ A_UCS^* displayed to the voter
    """
    electionString = ""
    candidateIndex = 0
    for j in range(len(k)):
        electionString += "# Election {}\n".format(j)
        for l in range(0,n[j]):
            electionString += "Candidate {}: {}\n".format(candidateIndex, c[candidateIndex])
            candidateIndex += 1
        electionString += "You can make {} selection(s) for this particular election\n\n".format(k[j])

    P = \
"""
Voting page for voter {i}:

Simultaneous elections:

{elections}

""".format(
        i=i,
        elections=electionString
    )
    return P


class GetVotingPageTest(unittest.TestCase):
    def testGetVotingPage(self):
        print(GetVotingPage(1,testparams.c,testparams.n,testparams.k))

if __name__ == '__main__':
    unittest.main()
