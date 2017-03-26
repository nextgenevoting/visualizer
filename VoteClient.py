from VotingClient.GetVotingPage             import GetVotingPage
from BulletinBoard                          import BulletinBoard
from VotingClient.GenBallot                 import GenBallot

class VoteClient(object):
    """
    The VoteClient class represents a voting client participating in the protocols (for example prot 6.5)
    """

    i = None
    bulletinBoard = None                # Reference to the bulletinBoard object
    k_i = None

    def __init__(self, i, bulletinBoard):
        self.i = i
        self.bulletinBoard = bulletinBoard

    def candidateSelection(self, secparams):
        """
        Protocol 6.4: Candidate selection

        Returns:
            list:       Selection
        """

        c,n,k,E = self.bulletinBoard.getCandidateSelectionParams()

        # Calculate eligibility vector
        self.k_i = []
        for j in range(len(k)):
            self.k_i.append(E[self.i][j] * k[j]) # if voter i is eligible to cast a vote in election j, multiply 1 * the number of selections in j

        # Get the voting page string
        P_i = GetVotingPage(self.i, c,n,self.k_i)

        print(P_i)
        s = input('Enter your selection : ')

        return [int(s) for s in s.split(',')]

    def castVote(self, s, secparams):
        pk = self.bulletinBoard.pk
        X = input('Enter your voting code: ')
        return GenBallot(X, s, pk, secparams)



