// initial state
const state = {
    elections: []
}


// mutations
const mutations = {
    SOCKET_SYNCELECTIONS: (state, data) => {
        console.log("SOCKET_SYNCELECTIONS called");
        state.elections = JSON.parse(data)
    }
}

export default {
    namespaced: true,
    state,
    mutations
}