from app.models.state import State

class ElectionAuthorityState(State):

    def __init__(self, j):
        self.j = j
        self.name = "ElectionAuthority{}".format(j)
        self.secretVotingCredentials = []
        self.publicVotingCredentials = []
        self.points = []

        # 7.3
        self.secretKeyShare = None      # sk_j
        self.publicKeyShare = None      # pk_j
        self.publicKey = None           # pk
