from chvote.Common.SecurityParams import secparams_l1
from app.models.electionAuthorityState import ElectionAuthorityState
from app.parties.ElectionAuthority import ElectionAuthority
from app.database import db
from app.parties.BulletinBoard import BulletinBoard
from app.parties.PrintingAuthority import PrintingAuthority


class VoteSimulator(object):

    def __init__(self, election):
        self.electionID = election
        self.secparams = secparams_l1
        self.authorities = [None] * self.secparams.s
        self.bulletinBoard = BulletinBoard(db.bulletinBoardStates, election)
        self.printingAuthority = PrintingAuthority(db.printingAuthorityStates, election)

        # create new election authorities
        for j in range(self.secparams.s):
            self.authorities[j] = ElectionAuthority(db.electionAuthorityStates, election, j)
            self.authorities[j].loadState()

    def persist(self):
        self.bulletinBoard.persist()
        for authority in self.authorities:
            authority.persist()

        self.printingAuthority.persist()

    def setupElection(self, v_bold, w_bold, c_bold, n_bold, k_bold):
        self.bulletinBoard.voters = v_bold
        self.bulletinBoard.countingCircles = w_bold
        self.bulletinBoard.candidates = c_bold
        self.bulletinBoard.numberOfCandidates = n_bold
        self.bulletinBoard.numberOfSelections = k_bold


        # 7.1 Generation of electorate data
        for authority in self.authorities:
            authority.GenElectionData(self.bulletinBoard, self.secparams)


        # 7.3 Key generation
        self.bulletinBoard.publicKeyShares = []

        for authority in self.authorities:
            publicKeyShare = authority.GenKey(self.bulletinBoard, self.secparams)
            self.bulletinBoard.publicKeyShares.append(publicKeyShare)
        for authority in self.authorities:
            pk = authority.GetPublicKey(self.bulletinBoard, self.secparams)
        self.bulletinBoard.publicKey = pk


    def printVotingCards(self):
        # 7.2 Printing of voting cards
        privateCredentials = []
        for authority in self.authorities:
            privateCredentials.append(authority.secretVotingCredentials)

        self.printingAuthority.privateCredentials = privateCredentials
        self.printingAuthority.PrintVotingCards(self.bulletinBoard, self.secparams)