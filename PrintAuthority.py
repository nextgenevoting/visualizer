from Crypto.SecurityParams              import secparams_default
from PrintingAuthority.GetVotingCards   import GetVotingCards
from BulletinBoard                      import BulletinBoard

class PrintingAuthority(object):
    """
    The PrintingAuthority class represents the printing authority
    """

    bulletinBoard = None

    def __init__(self, bulletinBoardRef):
        self.bulletinBoard = bulletinBoardRef

    def getVotingCards(self, D, secparams = secparams_default):
        """
        (Protocol 6.2) getVotingCards: Prints the voting sheets for all voters

        Args:
            V (list):   Voter description
            c (list):   List of candidate descriptions
            n (int):    Number of candidates
            k (int):    Number of selections
            E (list):   Eligibility Matrix
            D (tuple):  Code Sheet Data

        Returns:
            list:       code sheet
        """

        (s, rawSheetData) = GetVotingCards(self.bulletinBoard.v, self.bulletinBoard.c, self.bulletinBoard.n, self.bulletinBoard.k, self.bulletinBoard.E, D, secparams)

        return (s, rawSheetData)
