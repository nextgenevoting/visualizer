import Vue from 'vue'

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
  electionAuthorities: []
}

// mutations
const mutations = {
  SOCKET_SYNCELECTIONAUTHORITIES: (state, data) => {
    console.log('SOCKET_SYNCELECTIONAUTHORITIES called')
    state.electionAuthorities = JSON.parse(data)
  }
}

const actions = {
  setAutoMode ({ commit }, data) {
    debugger
    // this.electionAuthorities[data.electionAuthorityId].autoMode = data.newValue;
    Vue.http.post('setAutoMode', {
      'election': data.electionId,
      'authorityId': data.electionAuthorityId,
      'value': data.newValue
    }).then(response => {
      response.json().then((data) => {
        // success callback
      })
    }).catch(e => {
      this.$toasted.error(e.body.message)
    })
  }
}

const getters = {
  getElectionAuthority: (state, getters) => (id) => {
    for (let electionAuthority of state.electionAuthorities) {
      if (electionAuthority.id === id) { return electionAuthority }
    }
    return null
  },
  getBallots: (state, getters) => (id) => {
    // Returns the BallotList of an authority with authorityId == id
    let electionAuthority = getters.getElectionAuthority(id)
    if (electionAuthority !== null) { return electionAuthority.ballots } else { return [] }
  },
  getConfirmations: (state, getters) => (id) => {
    // Returns the ConfirmationList of an authority with authorityId == id
    let electionAuthority = getters.getElectionAuthority(id)
    if (electionAuthority !== null) { return electionAuthority.confirmations } else { return [] }
  },
  getConfirmationForVoter: (state, getters) => (voterId, electionId) => {
    // Returns the ConfirmationList of an authority with authorityId == id
    let electionAuthority = getters.getElectionAuthority(electionId)
    if (electionAuthority !== null) {
      for (let confirmation of electionAuthority.confirmations) {
        if (confirmation.voterId === voterId) { return confirmation }
      }
    }
    return null
  },
  getBallotsAndConfirmations: (state, getters) => (electionAuthorityId) => {
    let results = []
    debugger
    for (let ballot of getters.getBallots(electionAuthorityId)) {
      let confirmation = getters.getConfirmationForVoter(ballot.voterId, electionAuthorityId)
      results.push({voterId: ballot.voterId, ballot: ballot.ballot, confirmation: confirmation})
    }
    return results
  },
  getCheckBallotTasks: (state, getters) => (id) => {
    // Returns the checkBallotTasks of an authority with authorityId == id
    let electionAuthority = getters.getElectionAuthority(id)
    if (electionAuthority !== null) { return electionAuthority.checkBallotTasks } else { return [] }
  },
  getCheckConfirmationTasks: (state, getters) => (id) => {
    // Returns the checkConfirmationTasks of an authority with authorityId == id
    let electionAuthority = getters.getElectionAuthority(id)
    if (electionAuthority !== null) { return electionAuthority.checkConfirmationTasks } else { return [] }
  },
  hasCheckBallotTask: (state, getters) => (voterId) => {
    // checks if a given voter has a CheckBallotTask, returns the id of the election authority that has the check pending
    for (let auth of state.electionAuthorities) {
      for (let checkBallotTask of getters.getCheckBallotTasks(auth.id)) {
        if (checkBallotTask.voterId === voterId) { return auth.id }
      }
    }
    return -1
  },
  hasCheckConfirmationTask: (state, getters) => (voterId) => {
    // checks if a given voter has a CheckConfirmationTask, returns the id of the election authority that has the check pending
    for (let auth of state.electionAuthorities) {
      for (let checkConfirmationTask of getters.getCheckConfirmationTasks(auth.id)) {
        if (checkConfirmationTask.voterId === voterId) { return auth.id }
      }
    }
    return -1
  }
}

export default {
  state,
  mutations,
  actions,
  getters
}
