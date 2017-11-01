// initial state
const state = {
    electionAuthorities: [],
};

// mutations
const mutations = {
    SOCKET_SYNCELECTIONAUTHORITIES: (state, data) => {
        console.log('SOCKET_SYNCELECTIONAUTHORITIES called');
        state.electionAuthorities = JSON.parse(data);
    },
};

const getters = {
    getElectionAuthority:  (state, getters) => (id) => {
        for(let j in state.electionAuthorities) {
            let electionAuthority = state.electionAuthorities[j];
            if (electionAuthority.id === id)
                return electionAuthority;
        }
    },
    getVoterBallots:  (state, getters) => (id) => {
        // Returns the voterBallots of an authority with authorityId == id
        return getters.getElectionAuthority(id).voterBallots;
    },
    hasVoterBallot: (state, getters) => (voterId) => {
        // checks if a given voter has a VoterBallot, returns the id of the election authority that has the check pending
        debugger;
        for(let electionIndex in state.electionAuthorities){
            let authority = state.electionAuthorities[electionIndex];
            for (let voterBallotIndex in getters.getVoterBallots(authority.id)) {
                if(authority.voterBallots[voterBallotIndex].voterId === voterId)
                    return authority.id;
            }
        }
        return false;
    }


};

export default {
    state,
    mutations,
    getters
};
