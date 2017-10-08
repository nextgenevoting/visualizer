// initial state
const state = {
    count: 1,
    elections: []
}


// mutations
const mutations = {
    SOCKET_SYNCELECTIONDATA: (state, data) => {
        console.log("SOCKET_SYNCELECTIONDATA called");
        console.log(data);
        data = JSON.parse(data);
        state.count = data.counter;
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