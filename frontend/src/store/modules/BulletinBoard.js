// initial state
const state = {
        id: "",
        status: 0,
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
        state.status = data.status;

        var bb = JSON.parse(data.bulletinBoard);
        state.voters = bb.voters;
        state.candidates = bb.candidates;
        state.publicVotingCredentials = bb.publicCredentials;
        state.numberOfSelections = bb.numberOfSelections;
        state.publicKey = bb.publicKey;
    }
}

const getters = {
    getStatusText: ()=> {
        var statusId = state.status;
        switch(statusId){
            case 0:
                return "New";
                break;
            case 1:
                return "Electorate data generated";
                break;
            case 2:
                return "Voting Cards Printed";
                break;
            default:
                return "Unknown status";
        }

    }

}

export default {
    state,
    mutations,
    getters
}