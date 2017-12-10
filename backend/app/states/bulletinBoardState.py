from app.states.state import State

class BulletinBoardState(State):

    def __init__(self, electionID):
        self.electionID = electionID
        self.securityLevel = 1
        self.voters = []
        self.titles = []
        self.countingCircles = []
        self.candidates = []
        self.numberOfCandidates = []
        self.numberOfSelections = []
        self.numberOfParallelElections = 0
        self.eligibilityMatrix = []

        self.partialPublicVotingCredentials = []  # D_hat
        self.ballots = []
        self.confirmations = []

        # 6.3
        self.publicKeyShares = []
        self.publicKey = None

        # 6.7 Mixing
        self.encryptions = []
        self.shuffleProofs = []

        # 6.8
        self.decryptions = []
        self.decryptionProofs = []

        self.verificationResult = None