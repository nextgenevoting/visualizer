// initial state
const state = {
    count: 1,
    elections: []
}


// mutations
const mutations = {
    SOCKET_GETUPDATE: (state, data) => {
        console.log("SOCKET_GETUPDATE called");
        state.count = data.data.counter;
    },
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