// initial state
const state = {
    voters: [],
};

// mutations
const mutations = {
    SOCKET_SYNCVOTERS: (state, data) => {
        console.log('SOCKET_SYNCVOTERS called');
        state.voters = JSON.parse(data);
    },
};

export default {
    state,
    mutations,
};
