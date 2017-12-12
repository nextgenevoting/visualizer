import Vue from 'vue'
import vueInstance from '../../main.js'

/*
import { normalize, schema } from 'normalizr'

// Schema for normalization
const votingCard = new schema.Entity('votingCard')
const voter = new schema.Entity('voter', {
  votingCard: votingCard
})
const votersSchema = new schema.Array(voter)
*/

// initial state
const state = {
  voters: []
}

// mutations
const mutations = {
  SOCKET_SYNCVOTERS: (state, data) => {
    let json = JSON.parse(data)
    state.voters = json
  },
  SOCKET_VOTERMESSAGE: (state, data) => {
    if (vueInstance.$router.currentRoute.path.includes('/voter/') && parseInt(vueInstance.$router.currentRoute.params.voterId) === data.voterId) {
      Vue.toasted.error(data.message)
    }
  }
}

const getters = {
  getVoters: (state, getters) => () => {
    return state.voters
  },
  getVoter: (state, getters) => (id) => {
    return state.voters[id]
  },
  getVotingCard: (state, getters) => (id) => {
    if (state.voters[id].votingCard !== null) { return state.voters[id].votingCard } else { return null }
  }

}

export default {
  state,
  mutations,
  getters
}
