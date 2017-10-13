from app.models.state import State

class ElectionAuthorityState(State):

    def __init__(self, j):
        self.j = j
        self.name = "ElectionAuthority{}".format(j)
        self.secretVotingCredentials = []
        self.publicVotingCredentials = []
        self.points = []
