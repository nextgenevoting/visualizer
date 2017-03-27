from collections        import namedtuple

Ballot           = namedtuple("Ballot", "x_hat, a, b, pi")
BallotProof      = namedtuple("BallotProof", "t, s")
PublicValue      = namedtuple("PublicValue", "x_hat, a, b")
PublicCommitment = namedtuple("PublicCommitment", "t_1, t_2, t_3")
Point            = namedtuple("Point", "x, y")
Response         = namedtuple("Response", "b, c, d")
VotingSheet      = namedtuple("VotingSheet", "i, v, c, n, k_i, X, Y, FC, rc")
