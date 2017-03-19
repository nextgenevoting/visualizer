import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                    import AssertMpz, AssertList
from Crypto.SecurityParams          import secparams_default, secparams_l0
from Utils.ToInteger                import ToInteger
from VotingClient.GetSelectedPrimes import GetSelectedPrimes
from VotingClient.GenQuery          import GenQuery
from VotingClient.GenBallotProof    import GenBallotProof
from TestParams                     import testparams
from collections                    import namedtuple

Ballot = namedtuple("Ballot", "x_hat, a, b, pi")

def GenBallot(X, s, pk, secparams=secparams_default):
    """
    Algorithm 7.18: Generates a ballot based on the selection s and the voting code X. The
    ballot includes an OT query a and a proof pi. The algorithm also returns the random
    values used to generate the OT query. These random values are required in Alg. 7.27
    to derive the transferred messages from the OT response, which itself is generated by Alg. 7.25.

    Args:
        X (str):        Voting Code X ∈ A_X^l_X
        s (list):       Selection s = (s_1, ... , s_k), 1 <= s_1 < ... < s_k
        pk (mpz):       ElGamal key pk ∈ G_p \ {1}

    Returns:
        tuple:          (r, Ballot)
    """
    AssertMpz(pk)
    AssertList(s)

    x = mpz(ToInteger(X))
    x_hat = gmpy2.powmod(secparams.g_hat, x, secparams.p_hat)

    q = GetSelectedPrimes(s, secparams)                    # q = (q_1, ... , q_k)
    m = mpz(1)
    for i in range (len(q)):
        m = m * q[i]
    if m >= secparams.p: return None

    (a_query,r_query) = GenQuery(q, pk, secparams)
    a = r = mpz(1)
    for i in range(len(a_query)):
        a = (a * a_query[i]) % secparams.p
        r = (r * r_query[i]) % secparams.q
    b = gmpy2.powmod(secparams.g,r, secparams.p)
    pi = GenBallotProof(x,m,r,x_hat,a,b,pk, secparams)
    ballot = Ballot(x_hat,a,b,pi)

    return (ballot,r)

class GenBallotTest(unittest.TestCase):
    def testGenBallot(self):
        selection = [1,4]       # select candidates with indices 1,4
        (ballot, r) = GenBallot(testparams.X, selection, testparams.pk, secparams_l0)
        print(ballot)
        print(r)

if __name__ == '__main__':
    unittest.main()
