from Authority                              import Authority
from BulletinBoard                          import BulletinBoard
from Crypto.SecurityParams                  import secparams_default, secparams_l0, secparams_l1, secparams_l2, secparams_l3
from VoteClient                             import VoteClient
from PrintAuthority                         import PrintingAuthority
from VotingClient.CheckReturnCodes          import CheckReturnCodes
import json


class ProtocolRunner(object):

    jsonData = None
    bulletinBoard = None
    secparams = secparams_default
    authorities = []
    printingAuth = None
    voters = []

    def __init__(self, file):
        # read the profile json file
        with open(file) as data_file:
            self.jsonData = json.load(data_file)

        self.bulletinBoard = BulletinBoard()

        if self.jsonData["securityLevel"] == 0:
            self.secparams = secparams_l0
        elif self.jsonData["securityLevel"] == 1:
            self.secparams = secparams_l1
        elif self.jsonData["securityLevel"] == 2:
            self.secparams = secparams_l2
        elif self.jsonData["securityLevel"] == 3:
            self.secparams = secparams_l3
        else:
            self.secparams = secparams_default

        if self.jsonData["deterministicRandomGeneration"] == True:
            self.secparams.deterministicRandomGen = True

        # set up s authorites
        self.authorities = [Authority("S%d" % j) for j in range(self.secparams.s)]

        # extract voter names from json data
        self.voters = [voter["name"] for voter in self.jsonData["voters"]]

        self.printingAuth = PrintingAuthority(self.bulletinBoard)

    def run(self, autoInput = False):

        # ********** ELECTION PREPARATION PHASE **********
        # publish the data on the bulletin board
        self.bulletinBoard.setupElectionEvent(self.voters, self.jsonData["n"], self.jsonData["k"], self.jsonData["t"], self.jsonData["c"], self.jsonData["E"])
        print("Number of simultaneous elections: %d, of voters: %d, candidates: %d" %(self.bulletinBoard.t, self.bulletinBoard.N, self.bulletinBoard.n_sum))

        # Run Protocol 6.1: Election Preparation
        D_hat = [auth.generateElectionData(self.bulletinBoard.n, self.bulletinBoard.k, self.bulletinBoard.E, self.secparams) for auth in self.authorities]

        for auth in self.authorities:
            auth.calculatePublicCredentials(D_hat, self.secparams)
            auth.printPoints()

        # Run Protocol 6.2: Printing of Code Sheets

        D = [authority.d_j for authority in self.authorities]
        (sheets, rawSheetData) = self.printingAuth.getSheets(D, self.secparams)
        for sheet in sheets: print(sheet)

        # Run Protocol 6.3: Key Generation
        elgamalKeyshares = [authority.genKeyPair(self.secparams) for authority in self.authorities]
        for authority in self.authorities:
            self.bulletinBoard.pk = authority.getPublicKey(elgamalKeyshares, self.secparams)         # combine the resulting public key


        # ********** ELECTION PHASE **********
        # Run Protocol 6.4 & 6.5: Candidate Selection & Vote Casting
        votingClients = [VoteClient(i, self.jsonData["voters"][i], rawSheetData[i], self.bulletinBoard) for i in range(len(self.voters))]
        for votingClient in votingClients:

            # Get selection (6.4)
            s = votingClient.candidateSelection(autoInput, self.secparams)
            # Create ballot (6.5)
            (ballot,r) = votingClient.castVote(s, autoInput, self.secparams)

            # Check ballot (6.5)
            valid = True
            for authority in self.authorities:
                valid = valid and authority.runCheckBallot(votingClient.i,ballot, self.secparams)
                print("Ballot validity checked by authority %s: %r" % (authority.name, valid))

            beta = [authority.genResponse(votingClient.i,ballot.a, self.secparams)[0] for authority in self.authorities]
            P_s = votingClient.getPointsFromResponse(beta, self.secparams)
            print(P_s)
            returnCodes = votingClient.getReturnCodes(self.secparams)
            print(returnCodes)

            print("CheckReturnCodes: %r" %CheckReturnCodes(votingClient.votingSheet.rc, returnCodes, s))