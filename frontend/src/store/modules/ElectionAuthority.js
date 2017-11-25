import Vue from 'vue'

/*
 // if normalization is desired: Please remember that normalizr requires that every schema contains an id
 // since our API doesn't provide ids for ballots, encryptions etc., we would have generate some random ID on the client:
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
    state.electionAuthorities = JSON.parse(data)
  }
}

const actions = {
  setAutoMode ({ commit }, data) {
    Vue.http.post('setAutoMode', {
      'election': data.electionId,
      'authorityId': data.electionAuthorityId,
      'value': data.newValue
    }).then(response => {
      response.json().then((data) => {
      })
    }).catch(e => {
      this.$toasted.error(e.body.message)
    })
  }
}

const getters = {
  numberOfElectionAuthorities: (state, getters) => {
    return state.electionAuthorities.length
  },
  getElectionAuthority: (state, getters) => (id) => {
    for (let electionAuthority of state.electionAuthorities) {
      if (electionAuthority.id === id) { return electionAuthority }
    }
    return null
  },
  getBallots: (state, getters) => (authorityId) => {
    // Returns the BallotList of an authority with authorityId == id
    if (authorityId === null || authorityId === undefined) { return getters.getBallotsOfBulletinBoard } else {
      let electionAuthority = getters.getElectionAuthority(authorityId)
      if (electionAuthority !== null) { return electionAuthority.ballots } else { return [] }
    }
  },
  getConfirmations: (state, getters) => (id) => {
    // Returns the ConfirmationList of an authority with authorityId == id
    let electionAuthority = getters.getElectionAuthority(id)
    if (electionAuthority !== null) { return electionAuthority.confirmations } else { return [] }
  },
  getConfirmationForVoter: (state, getters) => (voterId, electionAuthorityId) => {
    // Returns the ConfirmationList of an authority with electionAuthorityId
    let confirmations = getters.getConfirmations(electionAuthorityId)
    for (let confirmation of confirmations) {
      if (confirmation.voterId === voterId) { return confirmation }
    }

    return null
  },
  getConfirmationsOfBallot: (state, getters) => (ballotId, electionAuthorityId) => {
    // Returns the ConfirmationList corresponding to some ballotId
    let confirmations = []
    if (electionAuthorityId === null) { confirmations = getters.getConfirmationsOfBulletinBoard } else { confirmations = getters.getConfirmations(electionAuthorityId) }

    let result = []
    for (let confirmation of confirmations) {
      if (confirmation.ballotId === ballotId) {
        result.push(confirmation)
      }
    }
    return result
  },
  getBallotsAndConfirmations: (state, getters) => (electionAuthorityId) => {
    let results = []
    for (let ballot of getters.getBallots(electionAuthorityId)) {
      ballot.confirmations = getters.getConfirmationsOfBallot(ballot.id, electionAuthorityId)
      results.push(ballot)
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
  hasMixingTask: (state, getters) => (id) => {
    let electionAuthority = getters.getElectionAuthority(id)
    if (getters.status === 4 && electionAuthority.encryptions.length > 0 && !getters.hasAuthorityMixed(id)) { return 1 } else { return 0 }
  },
  getNumberOfTasks: (state, getters) => (id) => {
    // returns the number of tasks for an authority
    return getters.getCheckBallotTasks(id).length + getters.getCheckConfirmationTasks(id).length + getters.hasMixingTask(id) + getters.hasDecryptionTask(id)
  },
  getNumberOfTasksForAllAuthorities: (state, getters) => {
    let count = 0
    for (let i = 0; i < 3; i++) {
      count += (getters.getCheckBallotTasks(i).length + getters.getCheckConfirmationTasks(i).length + getters.hasMixingTask(i) + getters.hasDecryptionTask(i))
    }
    return count
  },
  ballotCheckAuthorityIndex: (state, getters) => (voterId) => {
    // checks if a given voter has a CheckBallotTask, returns the id of the election authority that has the check pending
    for (let auth of state.electionAuthorities) {
      for (let checkBallotTask of getters.getCheckBallotTasks(auth.id)) {
        if (checkBallotTask.voterId === voterId) { return auth.id }
      }
    }
    return -1
  },
  confirmationCheckAuthorityIndex: (state, getters) => (voterId) => {
    // checks if a given voter has a CheckConfirmationTask, returns the id of the election authority that has the check pending
    for (let auth of state.electionAuthorities) {
      for (let checkConfirmationTask of getters.getCheckConfirmationTasks(auth.id)) {
        if (checkConfirmationTask.voterId === voterId) { return auth.id }
      }
    }
    return -1
  },
  hasAuthorityMixed: (state, getters) => (authorityId) => {
    let electionAuthority = getters.getElectionAuthority(authorityId)
    return electionAuthority.encryptionsShuffled.length > 0
  },
  haveAllAuthoritiesMixed: (state, getters) => {
    if (getters.numberOfElectionAuthorities === 0) return null
    return getters.hasAuthorityMixed(getters.numberOfElectionAuthorities - 1)
  },
  getEncryptionsForAuthority: (state, getters) => (authorityId) => {
    let electionAuthority = getters.getElectionAuthority(authorityId)
    let encSource = null
    if (electionAuthority.encryptionsShuffled.length > 0) {
      encSource = electionAuthority.encryptionsShuffled
    } else {
      encSource = electionAuthority.encryptions
    }
    let encryptions = []
    let i = 0
    for (let enc of encSource) {
      // combine the encryptions with the permutation. The permutation is required as a key for the shuffle transition animation
      encryptions.push({a: enc[0], b: enc[1], key: electionAuthority.permutation[i++]})
    }
    return encryptions
  }
}

export default {
  state,
  mutations,
  actions,
  getters
}
