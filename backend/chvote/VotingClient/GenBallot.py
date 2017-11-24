import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils                    import AssertMpz, AssertList, AssertClass, AssertString
from chvote.Common.SecurityParams import SecurityParams, secparams_l0
from chvote.Utils.ToInteger                import ToInteger
from chvote.VotingClient.GetSelectedPrimes import GetSelectedPrimes
from chvote.VotingClient.GenQuery          import GenQuery
from chvote.VotingClient.GenBallotProof    import GenBallotProof
from chvote.UnitTestParams                 import unittestparams
from chvote.Types                          import Ballot
from chvote.Utils.StringToInteger          import StringToInteger

def GenBallot(X, s, pk, secparams, manipulatedPublicCredential = None):
    """
    Algorithm 7.18: Generates a ballot based on the selection s and the voting code X. The
    ballot includes an OT query a and a proof pi. The algorithm also returns the random
    values used to generate the OT query. These random values are required in Alg. 7.27
    to derive the transferred messages from the OT response, which itself is generated by Alg. 7.25.

    Args:
        X (str):                            Voting Code X ∈ A_X^l_X
        s (list of int):                    Selection s = (s_1, ... , s_k), 1 <= s_1 < ... < s_k
        pk (mpz):                           ElGamal key pk ∈ G_p \ {1}
       secparams (SecurityParams):          Collection of public security parameters

    Returns:
        tuple:                              alpha = (r, Ballot) = (r, (x_hat, a, b, pi))
    """

    AssertMpz(pk)
    AssertList(s)
    AssertClass(secparams, SecurityParams)

    x = mpz(StringToInteger(X, secparams.A_X))
    x_hat = gmpy2.powmod(secparams.g_hat, x, secparams.p_hat)
    if manipulatedPublicCredential != None:
        x_hat = mpz(manipulatedPublicCredential)

    q_bold = GetSelectedPrimes(s, secparams)                    # q = (q_1, ... , q_k)
    
    m = mpz(1)
    for j in range(len(q_bold)):
        m = m * q_bold[j]

    if m >= secparams.p:
        return None

    (a_bold, r_bold) = GenQuery(q_bold, pk, secparams)
    a = mpz(1)
    b = mpz(1)
    r = mpz(0)

    for j in range(len(q_bold)):
        a = (a * a_bold[j][0]) % secparams.p
        b = (b * a_bold[j][1]) % secparams.p
        r = (r + r_bold[j]) % secparams.q

    e = (a, b)
    pi = GenBallotProof(x,m,r,x_hat,e,pk, secparams)
    alpha = Ballot(x_hat,a_bold,pi)

    return (alpha, r_bold)

class GenBallotTest(unittest.TestCase):
    def testGenBallot(self):
        selection = [1,4]       # select candidates with indices 1,4
        (ballot, r) = GenBallot(unittestparams.X, selection, unittestparams.pk, secparams_l0)
        print(ballot)
        print(r)

if __name__ == '__main__':
    unittest.main()
