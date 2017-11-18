<template>
  <v-container>
    <div v-if="this.$store.state.loaded">
      <ContentTitle icon="mdi-view-dashboard" :title="$t('overview')"></ContentTitle>
      <v-flex xy12 md12>
        <v-stepper color="blue" alt-labels :value="status + 1">
          <v-stepper-header>
            <v-stepper-step step="1" :complete="status >= 1">{{$t('ElectionStatus.status_1')}}</v-stepper-step>
            <v-divider></v-divider>
            <v-stepper-step step="2" :complete="status >= 2">{{$t('ElectionStatus.status_2')}}</v-stepper-step>
            <v-divider></v-divider>
            <!--<v-stepper-step step="3" :complete="status >= 3">{{$t('ElectionStatus.status_3')}}</v-stepper-step>
            <v-divider></v-divider>-->
            <v-stepper-step step="4" :complete="status >= 4">{{$t('ElectionStatus.status_4')}}</v-stepper-step>
            <v-divider></v-divider>
            <v-stepper-step step="5" :complete="status >= 5">{{$t('ElectionStatus.status_5')}}</v-stepper-step>
            <v-divider></v-divider>
            <v-stepper-step step="6" :complete="status >= 6">{{$t('ElectionStatus.status_6')}}</v-stepper-step>
            <v-divider></v-divider>
            <v-stepper-step step="7" :complete="status >= 7">{{$t('ElectionStatus.status_7')}}</v-stepper-step>
          </v-stepper-header>
        </v-stepper>
      </v-flex>
      <br>
      <v-btn v-if="1==2" color="primary" v-on:click="debugVotingSim">Debug VoteSim trigger</v-btn>
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
      statusText: 'statusText',
      status: 'status'
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
