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
    // Sets the auto-mode of an election authority.
    // Because of the asynchronous call, this cannot be done as a mutation, but an "action"
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
    // returns the number of election authorities (basically always 3)
    return state.electionAuthorities.length
  },
  getElectionAuthority: (state, getters) => (id) => {
    // returns the state of an election authority with given id (or null if it doesn't exist)
    for (let electionAuthority of state.electionAuthorities) {
      if (electionAuthority.id === id) { return electionAuthority }
    }
    return null
  },
  getBallots: (state, getters) => (authorityId) => {
    // Returns the BallotList of an authority with authorityId == id
    // if no election authority id is passed, the ballot list of the bulletin board is returned
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
    // Returns all confirmations of an authority ID (or the bulletin Board if no ID is passed) that correspond to some ballot Id
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
    // returns a new array containing all ballots (of either an election authority or the bulletin board if no param is passed)
    // and adds the corresponding confirmations to every ballot
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
    // Returns the mixingTasks of an authority with authorityId == id
    let electionAuthority = getters.getElectionAuthority(id)
    if (getters.status === 4 && electionAuthority.encryptions.length > 0 && !getters.hasAuthorityMixed(id)) { return 1 } else { return 0 }
  },
  getNumberOfTasks: (state, getters) => (id) => {
    // returns the number of tasks for an authority
    // this getter is used to display the red badge in the election authorities tab that displays the number of pending tasks
    return getters.getCheckBallotTasks(id).length + getters.getCheckConfirmationTasks(id).length + getters.hasMixingTask(id) + getters.hasDecryptionTask(id)
  },
  getNumberOfTasksForAllAuthorities: (state, getters) => {
    // Sums all pending tasks by calling getNumberOfTasks for all authorities
    // used to control the visibility of the red exclamation mark in the election authority tab
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
    // returns true or false whether an authority has already mixed
    let electionAuthority = getters.getElectionAuthority(authorityId)
    return electionAuthority.encryptionsShuffled.length > 0
  },
  haveAllAuthoritiesMixed: (state, getters) => {
    // returns true or false whether all authorities have already mixed
    if (getters.numberOfElectionAuthorities === 0) return null
    return getters.hasAuthorityMixed(getters.numberOfElectionAuthorities - 1)
  },
  getEncryptionsForAuthority: (state, getters) => (authorityId) => {
    // returns a list of encryptions of an authority
    // If the authority has already shuffled, returns the list of shuffled encryptions
    // otherwise returns the list of unshuffled encryptions
    let electionAuthority = getters.getElectionAuthority(authorityId)
    let encSource = null
    if (electionAuthority.encryptionsShuffled.length > 0) {
      encSource = electionAuthority.encryptionsShuffled
    } else {
      encSource = electionAuthority.encryptions
    }
    let encryptions = []
    let i = 0
    // create a new list with named properties .a and .b for easier lookup
    for (let enc of encSource) {
      // combine the encryptions with the permutation. The permutation is required as a key for the shuffle transition animation
      encryptions.push({a: enc[0], b: enc[1], key: electionAuthority.permutation[i++]})
    }
    return encryptions
  },
  getPublicVotingCredentials: (state, getters) => {
    // Returns the publicVotingCredentials
    let electionAuthority = getters.getElectionAuthority(0)
    if (electionAuthority !== null) { return electionAuthority.publicVotingCredentials[0] } else { return [] }
  }
}

export default {
  state,
  mutations,
  actions,
  getters
}
