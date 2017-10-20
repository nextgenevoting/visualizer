// initial state
const state = {
    elections: [],
}

// mutations
const mutations = {
    SOCKET_SYNCELECTIONS: (state, data) => {
        state.elections = JSON.parse(data);

    }
}

export default {
    state,
    mutations
}