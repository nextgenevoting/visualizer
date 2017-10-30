import { normalize, schema } from 'normalizr';

const votingCard = new schema.Entity('votingCard');

// Define your comments schema
const voter = new schema.Entity('voter', {
    votingCard: votingCard,
});

// Define your article
const votersSchema = new schema.Array(voter);


// initial state
const state = {
    voters: [],
    votingCards: []
};

// mutations
const mutations = {
    SOCKET_SYNCVOTERS: (state, data) => {
        console.log('SOCKET_SYNCVOTERS called');
        var json = JSON.parse(data);
        const normalizedData = normalize(json, votersSchema);
        state.voters = normalizedData.entities.voter;
        //Vue.set(state, voters, normalizedData.entities.voter);
        state.votingCards = normalizedData.entities.votingCard;
        //Vue.set(state, votingCards, normalizedData.entities.votingCards);
    },
};

const getters = {
    getVoters:  (state, getters) => () => {
        return state.voters;
    },
    getVoter:  (state, getters) => (id) => {
        return state.voters[id];
    },
    getVotingCard: (state, getters) => (id) => {
        if(state.voters[id].votingCard !== null)
            return state.votingCards[state.voters[id].votingCard];
        else
            return null;
    },

};

export default {
    state,
    mutations,
    getters
};
