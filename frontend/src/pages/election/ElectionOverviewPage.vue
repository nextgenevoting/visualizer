<template>
  <v-container>
    <div v-if="this.$store.state.loaded">
      <ContentTitle icon="mdi-view-dashboard" :title="$t('overview')"></ContentTitle>

      {{ $t('id') }}: <b>{{ electionId }}</b>
      <br>
      {{ $t('status') }}: <b>{{ statusText }}</b>
      <br>
      <br>
      <v-btn color="primary" v-on:click="debugVotingSim">Debug VoteSim trigger</v-btn>
    </div>
    <div v-else>
      <LoadingOverlay></LoadingOverlay>
    </div>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import joinRoomMixin from '../../mixins/joinRoomMixin.js'

export default {
  mixins: [joinRoomMixin],
  computed: {
    ...mapGetters({
      electionId: 'electionId',
      statusText: 'statusText'
    })
  },
  methods: {
    debugVotingSim: function (event) {
      this.$http.post('debugVotingSim', {
        'election': this.$route.params['electionId']
      }).then(response => {
        response.json().then((data) => {
          // success callback
        })
      }, response => {
        // error callback
      })
    }
  },
  watch: {
    // whenever question changes, this function will run
    status: function (newStatus) {
      console.log('Status Watcher:' + newStatus)
    }
  }
}
</script>
