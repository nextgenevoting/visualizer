import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils    import AssertList, AssertInt
from chvote.UnitTestParams import unittestparams

def GetVotingPage(v, c_bold, n_bold, k_bold):
    """
    Algorithm 7.17: Computes a string P in A_UCS^*, which represents the voting page displayed
    to voter. Specifying the details of presenting the information on the voting page is beyond
    the scope of this document.

    Args:
        v (int):         Voter index
        c_bold (list):   Candidate descriptions c = (C_1, ..., C_n), c_v ∈ A_UCS^*
        n_bold (list):   Number of candidates n =(n_1, ..., n_t), n_j >= 2
        k_bold (list):   Number of selections k = (k_1, ..., k_t), 0 <= k_j < n_j

    Returns:
        string:     String P ∈ A_UCS^* displayed to the voter
    """

    AssertInt(v)
    AssertList(c_bold)
    AssertList(n_bold)
    AssertList(k_bold)

    electionString = ""
    candidateIndex = 0

    for j in range(len(k_bold)):
        electionString += "# Election {}\n".format(j)

        for l in range(n_bold[j]):
            electionString += "Candidate {}: {}\n".format(candidateIndex, c_bold[candidateIndex])
            candidateIndex += 1

        electionString += "You can make {} selection(s) for this particular election\n\n".format(k_bold[j])

    P = \
"""
Voting page for voter {v}:

Simultaneous elections:

{elections}
""".format(
          v = v
        , elections = electionString
        )

    return P

class GetVotingPageTest(unittest.TestCase):
    def testGetVotingPage(self):
        print(GetVotingPage(1,unittestparams.c,unittestparams.n,unittestparams.k))

if __name__ == '__main__':
    unittest.main()
