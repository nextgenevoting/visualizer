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

def CheckBallot(i, alpha, pk, K, x_hat, B, secparams=secparams_default):
    """
    Algorithm 7.22: Checks if a ballot alpha obtained from voter i is valid. For this, voter i
    must not have submitted a valid ballot before, pi must be valid, and x_hat must be the public
    voting credential of voter i. Note that parameter checking |a|  ki for ki  °tj1 kij is an important initial step of this algorithm.

    Args:
        i (int):            Voter index
        alpha (Ballot):     Ballot
        pk (mpz):           Public Key
        K ([][]):           Number of selections
        x_hat (mpz):        Public voting credential
        B (list):           Ballot List

    Returns:
        bool
    """
    AssertInt(i)
    AssertClass(alpha, Ballot)
    AssertMpz(pk)
    AssertList(K)
    AssertList(x_hat)
    AssertList(B)
    AssertClass(secparams, SecurityParams)

    #TODO: Da der Voting Code noch nicht berechnet werden kann (GetVotingSheet), muss hier fix ein Wert eingetragen werden. Sprich der Wert von x_hat der im Ballot gespeichert ist, ist momentan noch falsch und entspricht dem VotingCode der TestParams
    if not HasBallot(i, B, secparams):
    #if not HasBallot(i,B, secparams) and x_hat[i] == alpha.x_hat:
        a = mpz(1)
        for i in range(len(alpha.a)):
            a = (a * alpha.a[i]) % secparams.p
        if CheckBallotProof(alpha.pi, alpha.x_hat, a, alpha.b, pk, secparams):
            return True
    return False


class CheckBallotTest(unittest.TestCase):
    def testCheckBallot(self):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
