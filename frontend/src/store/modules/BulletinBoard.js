// initial state
const state = {
  voters: null,
  candidates: null,
  publicVotingCredentials: null,
  numberOfSelections: null,
  numberOfCandidates: null,
  publicKey: null,
  countingCircles: null,
  eligibilityMatrix: null,
  numberOfParallelElections: null,
  encryptions: null,
  decryptions: null,
  shuffleProofs: null,
  decryptionProofs: null

}

// mutations
const mutations = {
  SOCKET_SYNCELECTIONDATA: (state, data) => {
    console.log('SOCKET_SYNCELECTIONDATA called')
    const bb = JSON.parse(data)
    console.log(bb)
    state.voters = bb.voters
    state.candidates = bb.candidates
    state.publicVotingCredentials = bb.publicVotingCredentials
    state.numberOfSelections = bb.numberOfSelections
    state.numberOfCandidates = bb.numberOfCandidates
    state.publicKey = bb.publicKey
    state.countingCircles = bb.countingCircles
    state.eligibilityMatrix = bb.eligibilityMatrix
    state.numberOfParallelElections = bb.numberOfParallelElections
    state.encryptions = bb.encryptions
    state.decryptions = bb.decryptions
    state.shuffleProofs = bb.shuffleProofs
    state.decryptionProofs = bb.decryptionProofs
  }
}

const getters = {
  getDecryptionsForAuthority: (state, getters) => (authorityId) => {
    if (state.decryptions.length < authorityId + 1) { return null }
    return state.decryptions[authorityId]
  }
}

export default {
  state,
  mutations,
  getters
}
