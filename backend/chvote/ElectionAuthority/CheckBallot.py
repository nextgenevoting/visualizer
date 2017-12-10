import os
import sys
import unittest
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Common.SecurityParams import SecurityParams, secparams_l0
from chvote.ElectionAuthority.HasBallot        import HasBallot
from chvote.ElectionAuthority.CheckBallotProof import CheckBallotProof
from chvote.Utils.Utils                        import AssertInt, AssertList, AssertMpz, AssertClass
from chvote.Types                              import Ballot, BallotProof
from chvote.VotingClient.GenBallot             import GenBallot
from chvote.UnitTestParams                     import unittestparams
from chvote.Types                              import *
from chvote.Common.IsMember                    import IsMember

def CheckBallot(v, alpha, pk, k_bold, E_bold, x_hat_bold, B, secparams):
    """
    Algorithm 7.22: Checks if a ballot alpha obtained from voter v is valid. For this, voter i
    must not have submitted a valid ballot before, pi must be valid, and x_hat must be the public
    voting credential of voter v. Note that parameter checking |a|  ki for ki  °tj1 kij is an important initial step of this algorithm.

    Args:
        v (int):                             Voter index
        alpha (Ballot):                      Ballot
        pk (mpz):                            Public Key
        k_bold (list):                       Number of selections
        E_bold (list):                       Eligibility matrix E
        x_hat_bold (list):                   Public voting credentials
        B (list):                            Ballot List
        secparams (SecurityParams):          Collection of public security parameters

    Returns:
        bool:                                True if the ballot is valid, False if not
    """

    AssertInt(v)
    AssertClass(alpha, Ballot)
    AssertMpz(pk)
    assert IsMember(pk, secparams), "pk must be in G_q"
    AssertList(k_bold)
    AssertList(x_hat_bold)
    AssertList(B)
    AssertClass(secparams, SecurityParams)

    k_prime = 0
    for j in range(len(k_bold)):
        k_prime = k_prime + E_bold[v][j] * k_bold[j]  # if voter i is eligible to cast a vote in election j, multiply 1 * the number of selections in j

    hasBallot = HasBallot(v,B, secparams)
    credentialCheck = x_hat_bold[v] == alpha.x_hat
    queryLength = len(alpha.a_bold) == k_prime
    if not hasBallot and credentialCheck and queryLength:
        ballotProofCheck = CheckBallotProof(alpha.pi, alpha.x_hat, alpha.a_bold, pk, secparams)
        if ballotProofCheck:
            return True, []


    return (False, [False, hasBallot, credentialCheck, queryLength])

class CheckBallotTest(unittest.TestCase):
    def testCheckBallot(self):
        selection = [1, 4]  # select candidates with indices 1,4
        (ballot, r) = GenBallot(unittestparams.X, selection, unittestparams.pk, secparams_l0)
        self.assertTrue(CheckBallot(0,ballot,unittestparams.pk,unittestparams.K,[unittestparams.x_hat],[],secparams_l0))

        # check if a ballot with more than the allowed number of selections fails
        selection = [1,2,3]  # select candidates with indices 1,4
        (ballot, r) = GenBallot(unittestparams.X, selection, unittestparams.pk, secparams_l0)
        self.assertFalse(CheckBallot(0,ballot,unittestparams.pk,unittestparams.K,[unittestparams.x_hat],[],secparams_l0))

        # check if a ballot with more than the allowed number of selections fails
        selection = [1,3]  # select candidates with indices 1,4
        (ballot, r) = GenBallot(unittestparams.X, selection, unittestparams.pk, secparams_l0)
        a_modified = ballot.a
        a_modified[0] += 1
        ballot_modified = Ballot(ballot.x_hat, a_modified, ballot.b, ballot.pi)
        self.assertFalse(CheckBallot(0,ballot_modified,unittestparams.pk,unittestparams.K,[unittestparams.x_hat],[],secparams_l0))

        # check if a ballot with more than the allowed number of selections fails
        selection = [1,3]  # select candidates with indices 1,4
        (ballot, r) = GenBallot(unittestparams.X, selection, unittestparams.pk, secparams_l0)
        ballot_modified = Ballot(ballot.x_hat, ballot.a, ballot.b + 1, ballot.pi)
        self.assertFalse(CheckBallot(0,ballot_modified,unittestparams.pk,unittestparams.K,[unittestparams.x_hat],[],secparams_l0))

        # check if a ballot with more than the allowed number of selections fails
        selection = [1,3]  # select candidates with indices 1,4
        (ballot, r) = GenBallot(unittestparams.X, selection, unittestparams.pk, secparams_l0)
        modified_proof = BallotProof(ballot.pi.t, (ballot.pi.s[0]+1, ballot.pi.s[1], ballot.pi.s[2]))
        ballot_modified = Ballot(ballot.x_hat, ballot.a, ballot.b, modified_proof)
        self.assertFalse(CheckBallot(0,ballot_modified,unittestparams.pk,unittestparams.K,[unittestparams.x_hat],[],secparams_l0))

if __name__ == '__main__':
    unittest.main()
