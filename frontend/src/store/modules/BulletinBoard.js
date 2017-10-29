// initial state
const state = {
  voters: null,
  candidates: null,
  publicVotingCredentials: null,
  numberOfSelections: null,
  publicKey: null,
  countingCircles: null,
};


// mutations
const mutations = {
  SOCKET_SYNCELECTIONDATA: (state, data) => {
    console.log('SOCKET_SYNCELECTIONDATA called');
    const bb = JSON.parse(data);
    state.voters = bb.voters;
    state.candidates = bb.candidates;
    state.publicVotingCredentials = bb.publicCredentials;
    state.numberOfSelections = bb.numberOfSelections;
    state.publicKey = bb.publicKey;
    state.countingCircles = bb.countingCircles;
  },
};

const getters = {

};

export default {
  state,
  mutations,
  getters,
};
