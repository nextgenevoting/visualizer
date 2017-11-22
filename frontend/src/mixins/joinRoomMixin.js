export default {
  created () {
    if (this.$store.getters.joinedElectionId !== this.$route.params['electionId']) { this.$socket.emit('join', {election: this.$route.params['electionId']}) }
  }
}
