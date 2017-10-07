// initial state
const state = {
    count: 1,
    message : "None",
    elections: []
}


// mutations
const mutations = {
    SOCKET_GETUPDATE: (state, data) => {
        console.log("SOCKET_GETUPDATE called");
        state.message = data.data.message;
        state.count = data.data.counter;
    },
    SOCKET_GETELECTIONS: (state, data) => {
        console.log("SOCKET_GETELECTIONS called");

        state.elections = JSON.parse(data)
    }
}

export default {
    namespaced: true,
    state,
    mutations
}