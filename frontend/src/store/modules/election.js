// initial state
const state = {
        id: "",
        status: 0,
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
        data = JSON.parse(data);
        state.count = data.counter;
    },
    SOCKET_SYNCELECTIONDATA: (state, data) => {
        console.log("SOCKET_SYNCELECTIONDATA called");
        state.id = data.election;
        state.status = data.status;

        var bb = JSON.parse(data.bulletinBoard);
        state.voters = bb.voters;
        state.candidates = bb.candidates;
        state.publicVotingCredentials = bb.publicCredentials;
        state.numberOfSelections = bb.numberOfSelections;
    }
}

export default {
    namespaced: false,
    state,
    mutations
}