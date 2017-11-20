from app.states.state import State

class ElectionAdministratorState(State):

    def __init__(self):
        self.votes = []        # V_bold
        self.w_bold = []       # W_bold
        self.finalResults = []