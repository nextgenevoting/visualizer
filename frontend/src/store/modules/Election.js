// initial state
const state = {
  elections: [],
  status: -1,
};

// mutations
const mutations = {
  SOCKET_SYNCELECTIONS: (state, data) => {
    state.elections = JSON.parse(data);
  },
  SOCKET_SYNCELECTION: (state, data) => {
    console.log('SOCKET_SYNCELECTION called');
    console.log(data);
    state.electionID = data.electionID;
    state.status = data.status;
  },

};


const getters = {
  getStatus: () =>{
    return state.status;
  },
  getStatusText: () => {
    const statusId = state.status;
    switch (statusId) {
      case 0:
        return 'New';
        break;
      case 1:
        return 'Electorate data generated';
        break;
      case 2:
        return 'Voting Cards Printed';
        break;
      case 3:
        return 'Voting Cards Delivered';
        break;
      default:
        return 'Unknown status';
    }
  },

};

export default {
  state,
  mutations,
  getters,
};
