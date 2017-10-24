// initial state
const state = {
    electionAuthorities: [],
};

// mutations
const mutations = {
    SOCKET_SYNCELECTIONAUTHORITIES: (state, data) => {
        console.log('SOCKET_SYNCELECTIONAUTHORITIES called');
        state.electionAuthorities = JSON.parse(data);
    },
};

const getters = {
    getElectionAuthority:  (state, getters) => (id) => {
        return state.electionAuthorities[id];
    },

};

export default {
    state,
    mutations,
    getters
};
