import { normalize, schema } from 'normalizr';
import cuid from 'cuid'
import Vue from 'vue';

/*
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
*/


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

const actions = {
    setAutoMode ({ commit }, data) {
        debugger;
        //this.electionAuthorities[data.electionAuthorityId].autoMode = data.newValue;
        Vue.http.post('setAutoMode', {
            'election': data.electionId,
            'authorityId': data.electionAuthorityId,
            'value': data.newValue
        }).then(response => {
            response.json().then((data) => {
                // success callback
            });
        }).catch(e => {
            this.$toasted.error(e.body.message);
        })
    }
}

const getters = {
    getElectionAuthority:  (state, getters) => (id) => {
        for(let electionAuthority of state.electionAuthorities) {
            if (electionAuthority.id === id)
                return electionAuthority;
        }
        return null;
    },
    getBallots:  (state, getters) => (id) => {
        // Returns the BallotList of an authority with authorityId == id
        let electionAuthority = getters.getElectionAuthority(id);
        if(electionAuthority !== null)
            return electionAuthority.ballots;
        else
            return [];
    },
    getVoterBallots:  (state, getters) => (id) => {
        // Returns the voterBallots of an authority with authorityId == id
        let electionAuthority = getters.getElectionAuthority(id);
        if(electionAuthority !== null)
            return electionAuthority.voterBallots;
        else
            return [];
    },
    hasVoterBallot: (state, getters) => (voterId) => {
        // checks if a given voter has a VoterBallot, returns the id of the election authority that has the check pending
        for(let auth of state.electionAuthorities){
            for (let voterBallot of getters.getVoterBallots(auth.id)) {
                if(voterBallot.voterId === voterId)
                    return auth.id;
            }
        }
        return -1;
    }
};

export default {
    state,
    mutations,
    actions,
    getters
};
