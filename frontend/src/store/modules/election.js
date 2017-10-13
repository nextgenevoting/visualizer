// initial state
const state = {
        count: 1,
        voters: [],
        candidates: [],
        publicVotingCredentials: [],
        numberOfSelections: [],

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
        data = JSON.parse(data);
        state.voters = data.voters;
        state.candidates = data.candidates;
        state.publicVotingCredentials = data.publicCredentials;
        state.numberOfSelections = data.numberOfSelections;
    }
}

export default {
    namespaced: false,
    state,
    mutations
}