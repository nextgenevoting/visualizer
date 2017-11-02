from collections import namedtuple

TBallot      = namedtuple("Ballot", "x_hat, a_bold, pi")
BallotProof = namedtuple("BallotProof", "t, s")
Point       = namedtuple("Point", "x, y")
Response    = namedtuple("Response", "b, C_bold, d")
#VotingSheet = namedtuple("VotingSheet", "i, v, c, n, k_i, X, Y, FC, rc")
SecretVoterData = namedtuple("SecretVoterData", "x_i, y_i, F_i, r_i")
ElGamalEncryption = namedtuple("ElGamalEncryption", "a, b")
Confirmation = namedtuple("Confirmation", "y_hat, pi")
ShuffleProof = namedtuple("ShuffleProof", "t, s, c_bold, c_hat_bold")
DecryptionProof = namedtuple("DecryptionProof", "t, s")

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

class VoterBallot(object):
    def __init__(self, voterId, ballot):
        self.voterId = voterId
        self.ballot = ballot
        self.checkResults = []


class BallotWithRandomizations(object):
    def __init__(self, voterId, ballot, randomizations):
        self.voterId = voterId
        self.ballot = ballot
        self.randomizations = randomizations