from chvote.Common.SecurityParams import secparams_l1, secparams_l2, secparams_l3
from app.states.electionAuthorityState import ElectionAuthorityState
from app.states.voterState import VoterState
from app.actors.ElectionAuthority import ElectionAuthority
from app.database import db, serializeState
from app.actors.BulletinBoard import BulletinBoard
from app.actors.PrintingAuthority import PrintingAuthority
from app.actors.Voter import Voter
from app.actors.ElectionAdministrator import ElectionAdministrator
from bson.objectid import ObjectId
from app.api.syncService import syncElection, SyncType
from chvote.VotingClient.GenBallot import GenBallot
from chvote.Types import *
from chvote.VotingClient.GetPointMatrix import GetPointMatrix
from chvote.VotingClient.GetReturnCodes import GetReturnCodes
from chvote.VotingClient.GetFinalizationCode import GetFinalizationCode
from chvote.VotingClient.GenConfirmation import GenConfirmation
from chvote.Verifier.CheckAllShuffleProofs import CheckAllShuffleProofs
from chvote.ElectionAuthority.CheckDecryptionProofs import CheckDecryptionProofs
from app.utils.JsonParser import mpzconverter
import app.utils.jsonpatch as jsonpatch
import json
from chvote.Common.IsMember                    import IsMember

class VoteService(object):

    # *************************************************************************************
    # *** Internal methods for loading/saving the states
    # *************************************************************************************

    # Constructor:
    # Set up the voteSim instance by instantiating all actors and loading the corresponding states from the database
    def __init__(self, electionID):
        self.electionID = electionID

        # load bulletinBoard
        self.bulletinBoard = BulletinBoard(db.bulletinBoardStates, electionID)

        if self.bulletinBoard.securityLevel == 2:
            self.secparams = secparams_l2
        elif self.bulletinBoard.securityLevel == 3:
            self.secparams = secparams_l3
        else:
            self.secparams = secparams_l1

        # load printing authority
        self.printingAuthority = PrintingAuthority(db.printingAuthorityStates, electionID)

        # load election administrator
        self.electionAdministrator = ElectionAdministrator(db.electionAdministratorStates, electionID)

        # load election authorities
        self.authorities = [None] * self.secparams.s
        for j in range(self.secparams.s):
            self.authorities[j] = ElectionAuthority(db.electionAuthorityStates, electionID, j)

        # load voters
        self.voters = []
        for i in range(len(self.bulletinBoard.voters)):
            self.voters.append(Voter(db.voterStates, electionID, i))

    def getJSONPatches(self):
        # todo: JSONPatch creation for the voter states is currently very cumbersome
        return {
            'bulletin_board':         self.bulletinBoard.getJSONPatch(),
            'printing_authority':     self.printingAuthority.getJSONPatch(),
            'election_administrator': self.electionAdministrator.getJSONPatch(),
            'election_authority_0':   self.authorities[0].getJSONPatch(),
            'election_authority_1':   self.authorities[1].getJSONPatch(),
            'election_authority_2':   self.authorities[2].getJSONPatch(),
            'voters':                 jsonpatch.make_patch(json.loads(json.dumps([ voter.originalState.__dict__ for voter in self.voters ], default=mpzconverter)), json.loads(json.dumps([ voter.state.__dict__ for voter in self.voters ], default=mpzconverter))).patch
        }

    # persist()
    # Save the state of all actors to the database
    def persist(self):
        patches = self.getJSONPatches()

        if (len(patches['bulletin_board']) > 0): self.bulletinBoard.persist()
        if (len(patches['printing_authority']) > 0): self.printingAuthority.persist()
        if (len(patches['election_administrator']) > 0): self.electionAdministrator.persist()
        if (len(patches['election_authority_0']) > 0): self.authorities[0].persist()
        if (len(patches['election_authority_1']) > 0): self.authorities[1].persist()
        if (len(patches['election_authority_2']) > 0): self.authorities[2].persist()
        if (len(patches['voters']) > 0):
            for voter in self.voters: voter.persist()

        revision = self.incrementRevision()
        return (patches, revision)

    # updateStatus()
    # Helper function to update the status of an election
    def updateStatus(self, newStatus):
        assert isinstance(newStatus, int), "status must be a number"
        db.elections.update_one({'_id': ObjectId(self.electionID)}, {"$set": {"status" : newStatus}}, upsert=False)
        syncElection(self.electionID, SyncType.ROOM)

    # incrementRevision()
    # Helper function to update the revisionnumber of an election
    def incrementRevision(self):
        election = db.elections.find_one({'_id': ObjectId(self.electionID)})
        if election != None:
            revNumber = election["revision"]
            newRevNumber = revNumber + 1
            db.elections.update_one({'_id': ObjectId(self.electionID)}, {"$set": {"revision": newRevNumber}}, upsert=False)
            return newRevNumber
        else:
            raise RuntimeError("Election not found")


    # *************************************************************************************
    # The following functions implement the chVote protocol
    # *************************************************************************************

    # setupElection()
    # Set the pre-election parameters and generate electorate data
    def setupElection(self, numberOfVoters, w_bold, c_bold, n_bold, k_bold, titles):
        self.bulletinBoard.countingCircles = w_bold
        self.bulletinBoard.candidates = c_bold
        self.bulletinBoard.numberOfCandidates = n_bold
        self.bulletinBoard.numberOfSelections = k_bold
        self.bulletinBoard.numberOfParallelElections = len(k_bold)
        self.bulletinBoard.titles = titles

        voters = []
        for v in range(numberOfVoters):
            newVoter = VoterState(v)
            newVoter.countingCircle = w_bold[v]
            db.voterStates.insert({'election': self.electionID, 'voterID': v, 'state': serializeState(newVoter)})
            voters.append(newVoter.name)
            self.voters.append(Voter(db.voterStates, self.electionID, v, newVoter))

        self.bulletinBoard.voters = voters

        self.bulletinBoard.generateEligibilityMatrix()

        # 6.1 Generation of electorate data
        for authority in self.authorities:
            self.bulletinBoard.partialPublicVotingCredentials.append(authority.GenElectionData(self.bulletinBoard, self.secparams))
        for authority in self.authorities:
            authority.GetPublicCredentials(self.bulletinBoard, self.secparams)

        # 6.3 Key generation
        self.bulletinBoard.publicKeyShares = []

        for authority in self.authorities:
            publicKeyShare = authority.genKey(self.bulletinBoard, self.secparams)
            self.bulletinBoard.publicKeyShares.append(publicKeyShare)
        for authority in self.authorities:
            pk = authority.getPublicKey(self.bulletinBoard, self.secparams)
        self.bulletinBoard.publicKey = pk
        # 6.2 Send secret voter data to the printing authority (this is typically done in the printVotingCards(), but since we want to show the secret voter data before printing the cards, we do it here)

        if not IsMember(pk, self.secparams):
            raise RuntimeError("Generated PublicKey is not in group G_q!")

        secretCredentials = [auth.partialSecretVotingCredentials for auth in self.authorities]
        self.printingAuthority.privateCredentials = secretCredentials


    def printVotingCards(self):
        # 6.2 Printing of voting cards
        self.printingAuthority.PrintVotingCards(self.bulletinBoard, self.secparams)

    def sendVotingCards(self):
        # 6.2 Printing of voting cards contd.
        for voter in self.voters:
            voter.votingCard = self.printingAuthority.votingCards[voter.id]   # id = index + 1  --> (1,2,3...)


    def castVote(self, voterId, selection, votingCode, manipulatedPublicCredential, manipulatedPublicKey):
        # 6.5 Vote Casting
        voter = self.voters[voterId]

        # reset previous votecasting data
        voter.responses = []
        voter.points = []

        # create a new checkBallotTask (a temporary ballot that will be passed to the authorities for checking)
        (ballot, r) = GenBallot(votingCode, selection, self.bulletinBoard.publicKey, self.secparams, manipulatedPublicCredential, manipulatedPublicKey)

        voterBallot = VoterBallot(voterId, ballot, None)

        # pass it to the first authority
        checkBallotTask = CheckBallotTask(voterId, voterBallot.id)
        checkBallotTask.checkResults = [None] * self.secparams.s
        self.authorities[0].checkBallotTasks.append(checkBallotTask)
        #self.authorities[0].ballots.append(ballot)
        self.bulletinBoard.ballots.append(voterBallot)

        voter.selection = selection
        voter.randomizations = r
        voter.invalidBallot = False # hide previous "cast failed" alert

        # if the first authority is set to autoCheck = true, check ballot and reply automatically, otherwise checkVote will be called by the user through the webapp later
        if(self.authorities[0].autoCheck): self.checkVote(checkBallotTask.ballotId, 0)

    def abortVote(self, voterId):
        voter = self.voters[voterId]
        voter.status = -1


    def confirmVote(self, voterId, ballotId, confirmationCode):
        # 6.6 Vote Confirmation
        voter = self.voters[voterId]

        # reset previous confirmation data
        voter.invalidConfirmation = False # hide previous "cast failed" alert

        # create a new checkConfirmationTask (a temporary confirmation that will be passed to the authorities for checking)
        confirmation = GenConfirmation(confirmationCode, voter.points, self.secparams)
        voterConfirmation = VoterConfirmation(voterId, ballotId, confirmation)
        # pass it to the first authority
        checkConfirmationTask = CheckConfirmationTask(voterId, ballotId, voterConfirmation.id )
        checkConfirmationTask.checkResults = [None] * self.secparams.s
        self.authorities[0].checkConfirmationTasks.append(checkConfirmationTask)

        self.bulletinBoard.confirmations.append(voterConfirmation)

        # if the first authority is set to autoCheck = true, check ballot and reply automatically, otherwise checkVote will be called by the user through the webapp later
        if(self.authorities[0].autoCheck): self.checkConfirmation(checkConfirmationTask.confirmationId, 0)

    def checkVote(self, ballotId, authorityId):
        # 6.5 Vote Casting
        authority = self.authorities[authorityId]

        checkResult = authority.checkBallot(ballotId, self.bulletinBoard, self.secparams)

        if authority.autoCheck:
            if checkResult:
                self.respond(ballotId, authorityId)
            else:
                self.discardBallot(ballotId, authorityId)

    def respond(self, ballotId, authorityId):
        # 6.5 Vote Casting
        authority = self.authorities[authorityId]

        (checkBallotTask, response) = authority.respond(ballotId, self.bulletinBoard, self.secparams)
        #voter.responses.append(response)
        ballot = self.bulletinBoard.getBallotById(ballotId)

        # pass checkBallotTask to the next authority
        if authorityId < self.secparams.s - 1:
            self.authorities[authorityId + 1].checkBallotTasks.append(checkBallotTask)
            if (self.authorities[authorityId + 1].autoCheck):
                self.checkVote(ballotId, authorityId + 1)
        else:
            # this was the last authority to check the ballot
            # Generate return codes
            if all(checkResult for checkResult in checkBallotTask.checkResults):
                voter = self.voters[ballot.voterId]
                voter.validBallot = ballot.id
                self.getReturnCodes(ballot.voterId, ballot.responses)


    def discardBallot(self, ballotId, authorityId):
        # 6.5 Vote Casting
        authority = self.authorities[authorityId]

        voterId = authority.discardBallot(ballotId, self.bulletinBoard, self.secparams)
        self.voters[voterId].invalidBallot = True

    def getReturnCodes(self, voterId, responses):
        voter = self.voters[voterId]

        P_s = GetPointMatrix(responses, voter.selection, voter.randomizations, self.secparams)
        voter.points = P_s
        voter.verificationCodes = GetReturnCodes(voter.selection, P_s, self.secparams)
        voter.status = 1

    def checkConfirmation(self, confirmationId, authorityId):
        # 6.6 Vote Confirmation
        authority = self.authorities[authorityId]
        #voter = self.voters[voterId]

        checkResult = authority.checkConfirmation(confirmationId, self.bulletinBoard, self.secparams)

        if authority.autoCheck:
            if checkResult:
                self.finalize(confirmationId, authorityId)
            else:
                self.discardConfirmation(confirmationId, authorityId)


    def finalize(self, confirmationId, authorityId):
        # 6.6 Vote Confirmation
        authority = self.authorities[authorityId]

        (checkConfirmationTask, finalizations) = authority.finalize(confirmationId, self.bulletinBoard, self.secparams)
        confirmation = self.bulletinBoard.getConfirmationById(confirmationId)

        # pass checkConfirmationTask to the next authority
        if authorityId < self.secparams.s - 1:
            self.authorities[authorityId + 1].checkConfirmationTasks.append(checkConfirmationTask)
            if (self.authorities[authorityId + 1].autoCheck):
                self.checkConfirmation(confirmationId, authorityId + 1)
        else:
            # this was the last authority to check the confirmation
            # Generate finalizationCode codes
            if all(checkResult for checkResult in checkConfirmationTask.checkResults):

                voter = self.voters[checkConfirmationTask.voterId]
                voter.validConfirmation = checkConfirmationTask.confirmationId
                self.getFinalizationCode(checkConfirmationTask.voterId, confirmation.finalizations)

    def getFinalizationCode(self, voterId, finalizations):
        voter = self.voters[voterId]
        voter.finalizationCode = GetFinalizationCode(finalizations, self.secparams)
        voter.status = 2

    def discardConfirmation(self, confirmationId, authorityId):
        # 6.5 Vote Casting
        authority = self.authorities[authorityId]

        voterId = authority.discardConfirmation(confirmationId, self.bulletinBoard, self.secparams)

        self.voters[voterId].invalidConfirmation = True

# *********************************
#  POST ELECTION PHASE
# *********************************
    def startMixing(self):
        # the first election authority must extract the encryptions from the ballot-list
        numOfEncryptions = self.authorities[0].getEncryptions(self.bulletinBoard, self.secparams)

        # set the permutation to 1,2,3,...,len(encryptions) inititially for the shuffle transition / animation
        permutation = [i for i in range(numOfEncryptions)]

        for electionAuthority in self.authorities:
            electionAuthority.permutation = permutation

            # remove all checkBallot- and checkConfirmation tasks
            for checkBallotTask in electionAuthority.checkBallotTasks:
                electionAuthority.checkBallotTasks.remove(checkBallotTask)
            for checkConfirmationTask in electionAuthority.checkConfirmationTasks:
                electionAuthority.checkConfirmationTasks.remove(checkConfirmationTask)

        if (self.authorities[0].autoCheck):
                self.mix(0)

    def mix(self, authorityId):
        if len(self.authorities[authorityId].encryptions) == 0:
            raise RuntimeError("This authority requires the encryptions of the previous authority!")

        e_shuffled = self.authorities[authorityId].mix(self.bulletinBoard, self.secparams)

        # pass e_shuffled to the next authority
        if authorityId < self.secparams.s - 1:
            self.authorities[authorityId + 1].encryptions = e_shuffled
            if (self.authorities[authorityId + 1].autoCheck):
                self.mix(authorityId + 1)
        else:
            # this was the last authority to mix
            pass


    def startDecryption(self):
        self.updateStatus(5)
        if (self.authorities[0].autoCheck):
            self.decrypt(0)

    def decrypt(self, authorityId):
        authority = self.authorities[authorityId]

        shuffleProofCheck = authority.decrypt(self.bulletinBoard, self.secparams)
        if not shuffleProofCheck:
            raise RuntimeError("Shuffle proof check failed!")

        if authorityId < self.secparams.s - 1:
            if (self.authorities[authorityId + 1].autoCheck):
                self.decrypt(authorityId+1)
        else:
            # this was the last authority to decrypt
            self.updateStatus(6)

    def tally(self):
        self.electionAdministrator.tally(self.bulletinBoard, self.secparams)

    def publishResult(self):
        self.updateStatus(7)

    def verifyElection(self):
        res = VerificationResult()

        # Shuffle Proofs Check
        res.shuffleProofsCheck = CheckAllShuffleProofs(self.bulletinBoard.shuffleProofs, self.authorities[0].encryptions, self.bulletinBoard.encryptions, self.bulletinBoard.publicKey, self.secparams)

        # Shuffle vector dimensions check
        shuffleDimensionCheck = True
        for auth in self.authorities:
            if len(auth.encryptions) != len(auth.encryptionsShuffled):
                shuffleDimensionCheck == False
        res.shuffleDimensionCheck = shuffleDimensionCheck

        # Decryption Proofs Check
        res.decryptionProofsCheck = CheckDecryptionProofs(self.bulletinBoard.decryptionProofs, self.bulletinBoard.publicKeyShares, self.bulletinBoard.encryptions[-1], self.bulletinBoard.decryptions, self.secparams )


        self.bulletinBoard.verificationResult = res

    def revealCode(self, voterId, codeIndex):
        voter = self.voters[voterId]
        if codeIndex == 0:
            voter.votingCodeRevealed = True
        if codeIndex == 1:
            voter.confirmationCodeRevealed = True