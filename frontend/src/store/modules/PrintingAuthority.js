// initial state
const state = {
  votingCards: [],
  privateCredentials: []
}

// mutations
const mutations = {
  SOCKET_SYNCPRINTINGAUTHORITY: (state, data) => {
    console.log('SOCKET_SYNCPRINTINGAUTHORITY called')

    const printingAuthorityState = JSON.parse(data)
    state.privateCredentials = printingAuthorityState.privateCredentials
    state.votingCards = printingAuthorityState.votingCards
  }
}

export default {
  state,
  mutations
}
