import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Crypto.SecurityParams              import SecurityParams, secparams_default, secparams_l0, secparams_l3
from ElectionAuthority.HasBallot        import HasBallot
from ElectionAuthority.CheckBallotProof import CheckBallotProof
from Utils.Utils                        import AssertInt, AssertList, AssertMpz, AssertClass
from Types                              import Ballot, BallotProof
from VotingClient.GenBallot             import GenBallot
from UnitTestParams                     import unittestparams
from Types                              import *

def CheckBallot(i, alpha, pk, K_bold, x_hat, B, secparams=secparams_default):
    """
    Algorithm 7.22: Checks if a ballot alpha obtained from voter i is valid. For this, voter i
    must not have submitted a valid ballot before, pi must be valid, and x_hat must be the public
    voting credential of voter i. Note that parameter checking |a|  ki for ki  °tj1 kij is an important initial step of this algorithm.

    Args:
        i (int):            Voter index
        alpha (Ballot):     Ballot
        pk (mpz):           Public Key
        K_bold ([][]):      Number of selections
        x_hat (list):       Public voting credential
        B (list):           Ballot List

    Returns:
        bool
    """

    AssertInt(i)
    AssertClass(alpha, Ballot)
    AssertMpz(pk)
    AssertList(K_bold)
    AssertList(x_hat)
    AssertList(B)
    AssertClass(secparams, SecurityParams)

    if not HasBallot(i,B, secparams) and x_hat[i] == alpha.x_hat:

        if len(alpha.a) != sum(K_bold[i]):   # check if the number of selections matches the sum of K[i]
            return False

        a = mpz(1)
        for j in range(len(alpha.a)):
            a = (a * alpha.a[j]) % secparams.p
        if CheckBallotProof(alpha.pi, alpha.x_hat, a, alpha.b, pk, secparams):
            return True
    return False

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

        # TODO: Checks of voting code and ballotList!

if __name__ == '__main__':
    unittest.main()
