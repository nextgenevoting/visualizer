// initial state
const state = {
  votes: [],
  finalResults: [],
  w_bold: []
}

// mutations
const mutations = {
  SOCKET_SYNCELECTIONADMINISTRATOR: (state, data) => {
    const electionAdministratorState = JSON.parse(data)
    state.votes = electionAdministratorState.votes
    state.w_bold = electionAdministratorState.w_bold
    state.finalResults = electionAdministratorState.finalResults
  }
}

export default {
  state,
  mutations
}
