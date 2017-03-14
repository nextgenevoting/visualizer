from VotingClient.GetVotingPage             import GetVotingPage
from BulletinBoard                          import BulletinBoard

class VoteClient(object):
    """
    The VoteClient class represents a voting client participating in the protocols (for example prot 6.5)
    """

    i = None
    bulletinBoard = None            # Reference to the bulletinBoard object

    def __init__(self, i, bulletinBoard):
        self.i = i
        self.bulletinBoard = bulletinBoard

    def candidateSelection(self):
        """
        Protocol 6.4: Candidate selection
        """

        c,n,k,E = self.bulletinBoard.getCandidateSelectionParams()

        # Calculate eligibility vector
        k_i = []
        for j in range(len(k)):
            k_i.append(E[self.i][j] * k[j]) # if voter i is eligible to cast a vote in election j, multiply 1 * the number of selections in j

        # Get the voting page string
        P_i = GetVotingPage(self.i, c,n,k_i)

        print(P_i)
        s = input('Enter your selection : ')

    def castVote(self):
        pass    # TODO (page 50)

