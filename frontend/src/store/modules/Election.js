// initial state
const state = {
  elections: [],
  status: -1,
  electionId: null
}

// mutations
const mutations = {
  SOCKET_SYNCELECTIONS: (state, data) => {
    state.elections = JSON.parse(data)
  },
  SOCKET_SYNCELECTION: (state, data) => {
    console.log('SOCKET_SYNCELECTION called')
    console.log(data)
    state.electionId = data.electionID
    state.status = data.status
  }

}

const getters = {
  electionId: () => {
    return state.electionId
  },
  status: () => {
    return state.status
  },
  statusText: () => {
    const statusId = state.status
    switch (statusId) {
      case 0:
        return 'New'
      case 1:
        return 'Electorate data generated'
      case 2:
        return 'Voting Cards Printed'
      case 3:
        return 'Voting Cards Delivered'
      default:
        return 'Unknown status'
    }
  }

}

export default {
  state,
  mutations,
  getters
}
