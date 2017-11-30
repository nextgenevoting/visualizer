import Vue from 'vue'
import Vuex from 'vuex'
import Election from './modules/Election'
import BulletinBoard from './modules/BulletinBoard'
import PrintingAuthority from './modules/PrintingAuthority'
import Voter from './modules/Voter'
import ElectionAuthority from './modules/ElectionAuthority'
import ElectionAdministrator from './modules/ElectionAdministrator'
import * as jsonpatch from 'fast-json-patch'

Vue.use(Vuex)

export const store = new Vuex.Store({
  namespaced: false,
  state: {
    connected: false,
    joinedElectionId: null,
    showConfidentiality: false,
    expertMode: false,
    selectedVoter: 0,
    selectedAuthority: 0,
    voterDialog: false,
    language: 'en',
    loaded: false
  },
  mutations: {
    SOCKET_PATCHSTATE: (state, data) => {
      // It seems that applying patches to the data store directly causes the reactivity to fail.
      // Vue.set seems to fix the problem; however, applying the patches to a lodash deepcopy and Vue.set'ting the copied object might be better
      const patches = JSON.parse(data)

      let deepCopy = Vue._.clone(state.BulletinBoard)
      jsonpatch.applyPatch(deepCopy, patches['bulletin_board'])
      Vue.set(state, 'BulletinBoard', deepCopy)

      deepCopy = Vue._.clone(state.PrintingAuthority)
      jsonpatch.applyPatch(deepCopy, patches['printing_authority'])
      Vue.set(state, 'PrintingAuthority', deepCopy)

      deepCopy = Vue._.clone(state.ElectionAdministrator)
      jsonpatch.applyPatch(deepCopy, patches['election_administrator'])
      Vue.set(state, 'ElectionAdministrator', deepCopy)

      for (let i = 0; i < 3; i++) {
        let deepCopy = Vue._.clone(state.ElectionAuthority.electionAuthorities[i])
        jsonpatch.applyPatch(deepCopy, patches[`election_authority_${i}`])
        Vue.set(state.ElectionAuthority.electionAuthorities, i, deepCopy)
      }

      deepCopy = Vue._.clone(state.Voter.voters)
      jsonpatch.applyPatch(deepCopy, patches['voters'])
      Vue.set(state.Voter, 'voters', deepCopy)
    },
    SOCKET_CONNECT: (state, data) => {
      // Called whenever a websocket connection is established
      state.connected = true
    },
    SOCKET_DISCONNECT: (state, data) => {
      // Called whenever a websocket connection is closed
      state.connected = false
      // reset joinedElectionId such that the next call of some election route will use the joinMixin to subscribe
      state.joinedElectionId = null
    },
    SOCKET_JOINACK: (state, electionId) => {
      // answer after join call. Remember joinedElectionId to prevent unnecessary join calls and initial data syncs
      state.joinedElectionId = electionId
      state.selectedVoter = 0
      state.loaded = true
    },
    selectedVoter: (state, selectedVoter) => {
      // Called whenever the selected voter has changed in the voter view
      state.selectedVoter = selectedVoter
    },
    selectedAuthority: (state, selectedAuthority) => {
      // Called whenever the selected election authority has changed in the election authorities view
      state.selectedAuthority = selectedAuthority
    },
    voterDialog: (state, value) => {
      // sets the visibility of the changeVoter dialog
      state.voterDialog = value
    },
    language: (state, value) => {
      // select language
      state.language = value
    },
    showConfidentiality: (state, value) => {
      // sets the visibility of the confidentiality chip
      state.showConfidentiality = value
    },
    expertMode: (state, value) => {
      // sets the expert mode setting (not used currently)
      state.expertMode = value
    }
  },
  getters: {
    joinedElectionId: (state, getters) => {
      // returns the ID of the joined election.
      return state.joinedElectionId
    }
  },
  modules: {
    Election,
    BulletinBoard,
    PrintingAuthority,
    Voter,
    ElectionAuthority,
    ElectionAdministrator
  }
})
