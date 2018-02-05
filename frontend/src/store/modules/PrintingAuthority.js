// initial state
const state = {
  votingCards: [],
  privateCredentials: []
}

// mutations
const mutations = {
  SOCKET_SYNCPRINTINGAUTHORITY: (state, data) => {
    const printingAuthorityState = JSON.parse(data)
    state.privateCredentials = printingAuthorityState.privateCredentials
    state.votingCards = printingAuthorityState.votingCards
    state.receivedData = printingAuthorityState.receivedData
  }
}

export default {
  state,
  mutations
}
