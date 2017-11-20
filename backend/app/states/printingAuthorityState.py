from app.states.state import State

class PrintingAuthorityState(State):

    def __init__(self):
        self.privateCredentials = []        # D_bold
        self.votingCards = []               # s
