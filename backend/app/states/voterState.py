from app.states.state import State

class VoterState(State):

    def __init__(self, id):
        self.id = id
        self.name = "Voter {}".format(id+1)
        self.votingCard = None
        self.countingCircle = None
        self.status = 0

        # voting client data
        self.selection = []
        self.randomizations = []
        self.validBallot = None
        self.invalidBallot = None
        self.invalidConfirmation = None
        self.points = []
        self.verificationCodes = []
        self.finalizations = []
        self.finalizationCode = ''

        self.votingCodeRevealed = None
        self.confirmationCodeRevealed = None