import Vue from 'vue'
import Vuex from 'vuex'
import Election from './modules/Election'
import BulletinBoard from './modules/BulletinBoard'
import PrintingAuthority from './modules/PrintingAuthority'
import Voter from './modules/Voter'
import ElectionAuthority from './modules/ElectionAuthority'

Vue.use(Vuex)

export const store = new Vuex.Store({
  namespaced: false,
  state: {
    connected: false,
    joinedElectionId: null,
    showConfidentiality: true,
    expertMode: false,
    selectedVoter: null,
    selectedAuthority: 0,
    voterDialog: false,
    language: 'en',
    loaded: false
  },
  mutations: {
    SOCKET_CONNECT: (state, data) => {
      state.connected = true
    },
    SOCKET_DISCONNECT: (state, data) => {
      state.connected = false
      state.joinedElectionId = null
    },
    SOCKET_JOINACK: (state, electionId) => {
      console.log('JOINACK')
      state.joinedElectionId = electionId
      state.selectedVoter = null
      state.loaded = true
    },
    selectedVoter: (state, selectedVoter) => {
      state.selectedVoter = selectedVoter
    },
    selectedAuthority: (state, selectedAuthority) => {
      state.selectedAuthority = selectedAuthority
    },
    voterDialog: (state, value) => {
      state.voterDialog = value
    },
    language: (state, value) => {
      state.language = value
    },
    showConfidentiality: (state, value) => {
      state.showConfidentiality = value
    },
    expertMode: (state, value) => {
      state.expertMode = value
    }
  },
  actions: {
    /* socket_getdata: (context, message) => {
            // console.log(message.data);
            context.commit('updateData', message.data);
        } */
  },
  getters: {
    joinedElectionId: (state, getters) => {
      return state.joinedElectionId
    }
  },
  modules: {
    Election,
    BulletinBoard,
    PrintingAuthority,
    Voter,
    ElectionAuthority
  }
})
