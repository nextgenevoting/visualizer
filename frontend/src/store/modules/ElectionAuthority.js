import { normalize, schema } from 'normalizr';
import cuid from 'cuid'

const processStrategy = value => {
    if (!Object.prototype.hasOwnProperty.call(value, 'uid')) value.uid = cuid();
    return {...value};
};

// Schema for normalization
const ballotSchema = new schema.Entity('ballot', undefined, {
    idAttribute: 'uid', processStrategy
});

const electionAuthoritySchema = new schema.Entity('voter', {
    ballots: [ballotSchema],
});
const electionAuthoritiesSchema = new schema.Array(electionAuthoritySchema);



// initial state
const state = {
    electionAuthorities: [],
};

// mutations
const mutations = {
    SOCKET_SYNCELECTIONAUTHORITIES: (state, data) => {
        console.log('SOCKET_SYNCELECTIONAUTHORITIES called');
        state.electionAuthorities = JSON.parse(data);
        const normalizedData = normalize(JSON.parse(data), electionAuthoritiesSchema);
        console.log(normalizedData);

    },
};

const getters = {
    getElectionAuthority:  (state, getters) => (id) => {
        debugger;
        for(let j in state.electionAuthorities) {
            let electionAuthority = state.electionAuthorities[j];
            if (electionAuthority.id === id)
                return electionAuthority;
        }
    },
    getBallots:  (state, getters) => (id) => {
        // Returns the BallotList of an authority with authorityId == id
        debugger;
        let electionAuthority = getters.getElectionAuthority(id);
        return electionAuthority.ballots;
    },
    getVoterBallots:  (state, getters) => (id) => {
        // Returns the voterBallots of an authority with authorityId == id
        return getters.getElectionAuthority(id).voterBallots;
    },
    hasVoterBallot: (state, getters) => (voterId) => {
        // checks if a given voter has a VoterBallot, returns the id of the election authority that has the check pending
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
