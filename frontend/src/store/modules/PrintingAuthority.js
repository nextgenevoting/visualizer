// initial state
const state = {
  votingCards: [],
};

// mutations
const mutations = {
  SOCKET_SYNCPRINTINGAUTHORITY: (state, data) => {
    console.log('SOCKET_SYNCPRINTINGAUTHORITY called');

    const printingAuthorityState = JSON.parse(data);
    state.votingCards = printingAuthorityState.votingCards;
  },
};

export default {
  state,
  mutations,
};
