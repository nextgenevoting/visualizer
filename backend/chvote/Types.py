from collections import namedtuple
import uuid
TBallot      = namedtuple("Ballot", "x_hat, a_bold, pi")
BallotProof = namedtuple("BallotProof", "t, s")
Point       = namedtuple("Point", "x, y")
Response    = namedtuple("Response", "b, C_bold, d")
#VotingSheet = namedtuple("VotingSheet", "i, v, c, n, k_i, X, Y, FC, rc")
SecretVoterData = namedtuple("SecretVoterData", "x_i, y_i, F_i, r_i")
ElGamalEncryption = namedtuple("ElGamalEncryption", "a, b")
TConfirmation = namedtuple("Confirmation", "y_hat, pi")
ShuffleProof = namedtuple("ShuffleProof", "t, s, c_bold, c_hat_bold")
DecryptionProof = namedtuple("DecryptionProof", "t, s")
from datetime import datetime

class VotingCard(object):
        def __init__(self, id, X, Y, FC, rc):
            self.id = id
            self.votingCode = X
            self.confirmationCode = Y
            self.verificationCodes = rc
            self.finalizationCode = FC


class Ballot(object):
    def __init__(self, x_hat, a_bold, pi):
        self.x_hat = x_hat
        self.a_bold = a_bold
        self.pi = pi

# temporary ballot generated by the voter, needs to be checked by the authorities before a real ballot will be created
class CheckBallotTask(object):
    def __init__(self, voterId, ballotId):
        self.voterId = voterId
        self.ballotId = ballotId
        self.checkResults = [None] * 3

# Ballot List entry: Ballot with Randomizations and voterID
class VoterBallot(object):
    def __init__(self, voterId, ballot, randomizations):
        self.id = str(uuid.uuid4())
        self.voterId = voterId
        self.ballot = ballot
        self.randomizations = randomizations
        self.validity = 0   # 0 = unchecked, 1 = valid, 2 = ballot proof failed, 3 = credential failed, 4 = voter already has a ballot
        self.responses = [None] * 3
        self.timestamp = datetime.now().strftime("%d. %b %Y %H:%M:%S")

# Confirmation List entry: Confirmation
class Confirmation(object):
    def __init__(self, y_hat, pi):
        self.y_hat = y_hat
        self.pi = pi

# temporary confirmation generated by the voter, needs to be checked by the authorities before a real confirmation will be created
class CheckConfirmationTask(object):
    def __init__(self, voterId, ballotId, confirmationId):
        self.voterId = voterId
        self.ballotId = ballotId
        self.confirmationId = confirmationId
        self.checkResults = [None] * 3

class VoterConfirmation(object):
    def __init__(self, voterId, ballotId, confirmation):
        self.voterId = voterId
        self.id = str(uuid.uuid4())
        self.ballotId = ballotId
        self.confirmation = confirmation
        self.validity = 0
        self.finalizations = [None] * 3
        self.timestamp = datetime.now().strftime("%d. %b %Y %H:%M:%S"
)