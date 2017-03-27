from Authority                              import Authority
from BulletinBoard                          import BulletinBoard
from Crypto.SecurityParams                  import secparams_default, secparams_l0, secparams_l1, secparams_l2, secparams_l3
from VoteClient                             import VoteClient
from PrintAuthority                         import PrintingAuthority
import json


class ProtocolRunner(object):

    jsonData = None
    bulletinBoard = None
    secparams = secparams_default
    authorities = []

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

        # set up s authorites
        self.authorities = [Authority("S%d" % j) for j in range(self.secparams.s)]


    def run(self, autoInput = False):

        # extract voter names from json data
        voters = [voter["name"] for voter in self.jsonData["voters"]]

        # publish the data on the bulletin board
        self.bulletinBoard.setupElectionEvent(voters, self.jsonData["n"], self.jsonData["k"], self.jsonData["t"], self.jsonData["c"], self.jsonData["E"])
        print("Number of simultaneous elections: %d, of voters: %d, candidates: %d" %(self.bulletinBoard.t, self.bulletinBoard.N, self.bulletinBoard.n_sum))

        # TODO: Run Protocol 6.1: Election Preparation
        D_hat = []
        print("Generate electorate data")
        for authority in self.authorities:
            D_hat.append(authority.generateElectionData(self.bulletinBoard.n, [1,1], self.bulletinBoard.E, self.secparams))
        for authority in self.authorities:
            authority.calculatePublicCredentials(D_hat, self.secparams)

        # TODO: Run Protocol 6.2: Printing of Code Sheets
        printAuth = PrintingAuthority(self.bulletinBoard)
        D = [authority.d_j for authority in self.authorities]
        (sheets, rawSheetData) = printAuth.getSheets(D, self.secparams)
        print("Printing voting sheets:\n")
        for sheet in sheets: print(sheet)

        # TODO: Run Protocol 6.3: Key Generation
        # Generate ElGamal key shares
        pk_shares = [authority.genKeyPair(self.secparams) for authority in self.authorities]
        # combine the resulting public key
        for authority in self.authorities:
            self.bulletinBoard.pk = authority.getPublicKey(pk_shares, self.secparams)

        # TODO: Run Protocol 6.4 & 6.5: Candidate Selection & Vote Casting
        votingClients = []
        for i in range(0, len(voters)):
            votingClient = VoteClient(i, self.jsonData["voters"][i], rawSheetData[i], self.bulletinBoard)
            votingClients.append(votingClient)

            # Get selection (6.4)
            s = votingClient.candidateSelection(autoInput, self.secparams)

            # Create ballot (6.5)
            (ballot,r) = votingClient.castVote(s, autoInput, self.secparams)
            proof = ballot.pi
            # Check ballot (6.5)
            for authority in self.authorities:
                valid = authority.runCheckBallot(i,ballot, self.secparams)
                print("Ballot Proof validity checked by authority %s: %r" % (authority.name, valid))
