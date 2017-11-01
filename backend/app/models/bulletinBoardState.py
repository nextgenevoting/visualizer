from app.models.state import State

class BulletinBoardState(State):

    def __init__(self, electionID):
        self.electionID = electionID
        self.voters = []
        self.countingCircles = []
        self.candidates = []
        self.numberOfCandidates = []
        self.numberOfSelections = []
        self.numberOfParallelElections = 0
        self.eligibilityMatrix = []

        self.publicCredentials = []
        self.ballots = []
        self.confirmations = []

        # 7.3
        self.publicKeyShares = []
        self.publicKey = None