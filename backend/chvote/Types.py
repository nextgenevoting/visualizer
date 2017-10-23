from collections import namedtuple

Ballot      = namedtuple("Ballot", "x_hat, a_bold, pi")
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
        def __init__(self, v, X, Y, FC, rc):
            self.voter = v
            self.votingCode = X
            self.confirmationCode = Y
            self.verificationCodes = rc
            self.finalizationCode = FC
