from app.states.state import State

class ElectionAuthorityState(State):

    def __init__(self, id):
        self.id = id
        self.name = "ElectionAuthority{}".format(id+1)
        self.autoCheck = False
        self.partialSecretVotingCredentials = []
        self.partialPublicVotingCredentials = []
        self.points = []

        self.publicVotingCredentials = []

        # 6.3
        self.secretKeyShare = None      # sk_j
        self.publicKeyShare = None      # pk_j
        self.publicKey = None           # pk

        # 6.4 & 6.5
        self.checkBallotTasks = []       # temporary store for ballots that need to be verified / responded to
        self.ballots = []                # ballot list
        self.checkConfirmationTasks = [] # temporary store for confirmations that need to be checked
        self.confirmations = []          # confirmation list

        # 6.7 Mixing
        self.encryptions = []
        self.permutation = []
        self.encryptionsShuffled = []