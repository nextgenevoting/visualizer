// initial state
const state = {
  electionID: null,
  voters: null,
  candidates: null,
  titles: null,
  partialPublicVotingCredentials: null,
  numberOfSelections: null,
  numberOfCandidates: null,
  publicKey: null,
  countingCircles: null,
  eligibilityMatrix: null,
  numberOfParallelElections: null,
  publicKeyShares: [],
  ballots: [],
  confirmations: [],
  encryptions: [],
  decryptions: [],
  shuffleProofs: [],
  decryptionProofs: []
}

// mutations
const mutations = {
  SOCKET_SYNCBULLETINBOARD: (state, data) => {
    const bb = JSON.parse(data)
    state.voters = bb.voters
    state.candidates = bb.candidates
    state.titles = bb.titles
    state.partialPublicVotingCredentials = bb.partialPublicVotingCredentials
    state.numberOfSelections = bb.numberOfSelections
    state.numberOfCandidates = bb.numberOfCandidates
    state.publicKeyShares = bb.publicKeyShares
    state.publicKey = bb.publicKey
    state.countingCircles = bb.countingCircles
    state.eligibilityMatrix = bb.eligibilityMatrix
    state.numberOfParallelElections = bb.numberOfParallelElections
    state.ballots = bb.ballots
    state.confirmations = bb.confirmations
    state.encryptions = bb.encryptions
    state.decryptions = bb.decryptions
    state.shuffleProofs = bb.shuffleProofs
    state.decryptionProofs = bb.decryptionProofs
    state.verificationResult = bb.verificationResult
  }
}

const getters = {
  getBallotsOfBulletinBoard: (state, getters) => {
    // returns the ballotlist of the bulletin board
    return state.ballots
  },
  getBallotById: (state, getters) => (ballotId) => {
    for (let ballot of getters.getBallotsOfBulletinBoard) {
      if (ballot.id === ballotId) {
        return {ballot: ballot}
      }
    }
  },
  getConfirmationById: (state, getters) => (confirmationId) => {
    for (let confirmation of getters.getConfirmationsOfBulletinBoard) {
      if (confirmation.id === confirmationId) {
        return {confirmation: confirmation}
      }
    }
  },
  getConfirmationsOfBulletinBoard: (state, getters) => {
    // returns the confirmation list of the bulletin board
    return state.confirmations
  },
  getDecryptionsForAuthority: (state, getters) => (authorityId) => {
    // returns the list of decryptions of a given election authority
    if (state.decryptions.length < authorityId + 1) { return null }
    return state.decryptions[authorityId]
  },
  hasDecryptionTask: (state, getters) => (authorityId) => {
    // returns true or false depending on whether the passed election authority has a pending decryption task
    if (getters.status !== 5) return 0
    if (authorityId === 0) { return getters.getDecryptionsForAuthority(authorityId) === null } else {
      return getters.getDecryptionsForAuthority(authorityId) === null && getters.getDecryptionsForAuthority(authorityId - 1) !== null
    }
  },
  haveAllAuthoritiesDecrypted: (state, getters) => {
    // returns true or false depending on whether all authorities have finished decrypting
    return getters.getDecryptionsForAuthority(getters.numberOfElectionAuthorities - 1) !== null
  }
}

export default {
  state,
  mutations,
  getters
}
