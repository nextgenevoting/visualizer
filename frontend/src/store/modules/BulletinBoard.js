// initial state
const state = {
        id: "",
        voters: [],
        candidates: [],
        publicVotingCredentials: [],
        numberOfSelections: [],
        publicKey: 0,

}


// mutations
const mutations = {
    SOCKET_SYNCELECTIONDATA: (state, data) => {
        console.log("SOCKET_SYNCELECTIONDATA called");
        console.log(data);
        state.id = data.election;

        var bb = JSON.parse(data.bulletinBoard);
        state.voters = bb.voters;
        state.candidates = bb.candidates;
        state.publicVotingCredentials = bb.publicCredentials;
        state.numberOfSelections = bb.numberOfSelections;
        state.publicKey = bb.publicKey;
    }
}

const getters = {

}

export default {
    state,
    mutations,
    getters
}