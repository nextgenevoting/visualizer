from chvote.Types import VotingCard, Ballot, VoterBallot, CheckBallotTask, Confirmation, CheckConfirmationTask, VoterConfirmation
import unittest
from gmpy2 import mpz

def mpzconverter(o):
    if o.__class__.__name__ == 'mpz':
        return str(o)

    if isinstance(o, bytearray):
        return str(o)

    if isinstance(o, bytes):
        return str(o)

    from app.models.voterState import VoterState
    from app.models.electionAuthorityState import ElectionAuthorityState
    from app.database import Testobj

    if isinstance(o, VoterState) or isinstance(o, ElectionAuthorityState) or isinstance(o, VotingCard) or isinstance(o, Ballot) or isinstance(o, VoterBallot) or isinstance(o, CheckBallotTask) or isinstance(o, VoterConfirmation) or isinstance(o, Confirmation) or isinstance(o, CheckConfirmationTask) or isinstance(o, Testobj):
        return o.__dict__



class mpzconverterTest(unittest.TestCase):
    def testMpzConversion(self):
        import json

        testObj = mpz(5)
        testJson = json.dumps(testObj, default=mpzconverter)
        self.assertTrue(testJson == '"5"')

if __name__ == '__main__':
    unittest.main()
