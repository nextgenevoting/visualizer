// initial state
const state = {
        count: 1
}


// mutations
const mutations = {
    SOCKET_SYNCCOUNTER: (state, data) => {
        console.log("SOCKET_SYNCCOUNTER called");
        console.log(data);
        data = JSON.parse(data);
        state.count = data.counter;
    },
    SOCKET_SYNCELECTIONDATA: (state, data) => {
        console.log("SOCKET_SYNCELECTIONDATA called");
        console.log(data);
        data = JSON.parse(data);
        state.voters = data.v;
        state.candidates = data.c;
    }
}

export default {
    namespaced: true,
    state,
    mutations
}