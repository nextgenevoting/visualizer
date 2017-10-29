from app.models.state import State

class VoterState(State):

    def __init__(self, id):
        self.id = id
        self.name = "Voter {}".format(id)
        self.votingCard = None
        self.countingCircle = None
        self.status = 0