// initial state
const state = {
  electionID: null,
  voters: null,
  candidates: null,
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
  SOCKET_SYNCELECTIONDATA: (state, data) => {
    const bb = JSON.parse(data)
    state.voters = bb.voters
    state.candidates = bb.candidates
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
  }
}

const getters = {
  getBallotsOfBulletinBoard: (state, getters) => {
    return state.ballots
  },
  getConfirmationsOfBulletinBoard: (state, getters) => {
    return state.confirmations
  },
  getDecryptionsForAuthority: (state, getters) => (authorityId) => {
    if (state.decryptions.length < authorityId + 1) { return null }
    return state.decryptions[authorityId]
  },
  hasDecryptionTask: (state, getters) => (authorityId) => {
    if (getters.status !== 5) return 0
    if (authorityId === 0) { return getters.getDecryptionsForAuthority(authorityId) === null } else {
      return getters.getDecryptionsForAuthority(authorityId) === null && getters.getDecryptionsForAuthority(authorityId - 1) !== null
    }
  },
  haveAllAuthoritiesDecrypted: (state, getters) => {
    return getters.getDecryptionsForAuthority(getters.numberOfElectionAuthorities) !== null
  }
}

export default {
  state,
  mutations,
  getters
}
