// initial state
const state = {
        id: "",
        status: 0,
        voters: [],
        candidates: [],
        publicVotingCredentials: [],
        numberOfSelections: [],

}


// mutations
const mutations = {
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

const getters = {
    getStatus: ()=> {
        var statusId = state.status;
        if (statusId == 0)
            return "Created";
        if (statusId == 1)
            return "Electorate data generated";
    }

}

export default {
    state,
    mutations,
    getters
}