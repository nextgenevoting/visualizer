// initial state
const state = {
  id: '',
  voters: [],
  candidates: [],
  publicVotingCredentials: [],
  numberOfSelections: [],
  publicKey: 0,
  countingCircles: [],
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