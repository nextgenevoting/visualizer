from app.models.state import State

class ElectionAuthorityState(State):

    def __init__(self, id):
        self.id = id
        self.name = "ElectionAuthority{}".format(id)
        self.secretVotingCredentials = []
        self.publicVotingCredentials = []
        self.points = []

        # 6.3
        self.secretKeyShare = None      # sk_j
        self.publicKeyShare = None      # pk_j
        self.publicKey = None           # pk

        # 6.4
        self.voterBallots = []           # temporary store for ballots that need to be verified / responded to
