<template>
    <v-container grid-list-md>
        <div v-if="this.$store.state.loaded">
            <ContentTitle icon="mdi-account-key" :title="$t('ElectionAdmin.title')"></ContentTitle>

            <div v-if="status == 0">
                <v-form v-model="valid" ref="form" lazy-validation>
                    <v-text-field :label="$t('candidates')" v-model="candidates" required></v-text-field>
                    <v-text-field :label="$t('number_of_voters')" v-model="numberOfVoters" required></v-text-field>
                    <v-text-field :label="$t('number_of_candidates')" v-model="numberOfCandidates" required></v-text-field>
                    <v-text-field :label="$t('number_of_selections')" v-model="numberOfSelections" required></v-text-field>
                    <v-text-field :label="$t('counting_circles')" v-model="countingCircles" required></v-text-field>

                    <v-btn color="primary" v-on:click="setUpElection" :disabled="!valid">
                      {{ $t('ElectionAdmin.set_up_election') }}
                    </v-btn>
                    <v-btn @click="clear">
                      {{ $t('clear') }}
                    </v-btn>
                </v-form>
            </div>

            <div v-if="status == 1 || status == 2" v-t="'ElectionAdmin.submitted_to_printing_authority'"></div>

            <div v-if="status == 3">
                <v-btn @click="startMixingPhase()">{{ $t('ElectionAdmin.end_election_phase') }}</v-btn>
            </div>

            <div v-if="status == 4">
                <v-btn @click="startDecryptionPhase()">{{ $t('ElectionAdmin.start_decryption_process') }}</v-btn>
            </div>

            <div v-if="status == 6">
                <v-btn @click="tally()">{{ $t('tally') }}</v-btn>

                <h5 v-t="'post_election_data'"></h5>
                <v-layout row wrap>
                    <v-flex xy12 md4>
                        <DataCard :title="$t('votes')" :expandable=false confidentiality="public">{{ votes }}</DataCard>
                    </v-flex>
                    <v-flex xy12 md4>
                        <DataCard :title="$t('final_results')" :expandable=false confidentiality="public">{{ finalResults }}</DataCard>
                    </v-flex>
                </v-layout>
            </div>
        </div>
        <div v-else>
            <LoadingOverlay></LoadingOverlay>
        </div>
    </v-container>
</template>

<script>
import { mapGetters, mapState } from 'vuex'
import joinRoomMixin from '../../mixins/joinRoomMixin.js'

export default {
  mixins: [joinRoomMixin],
  data: () => ({
    valid: true,
    candidates: '["Yes", "No", "Maybe"]',
    numberOfVoters: '5',
    numberOfSelections: '[1]',
    numberOfCandidates: '[3]',
    countingCircles: '[1,1,1,1,1]'
  }),
  computed: {
    ...mapGetters({
      electionId: 'electionId',
      status: 'status'
    }),
    ...mapState({
      votes: state => state.ElectionAdministrator.votes,
      w_bold: state => state.ElectionAdministrator.w_bold,
      finalResults: state => state.ElectionAdministrator.finalResults
    })
  },
  methods: {
    setUpElection (event) {
      if (this.$refs.form.validate()) {
        // this.$socket.emit('setUpElection', {'election': this.$route.params["id"]});
        this.$http.post('setUpElection',
          {
            'election': this.$route.params['electionId'],
            'numberOfVoters': this.numberOfVoters,
            'candidates': this.candidates,
            'numberOfCandidates': this.numberOfCandidates,
            'numberOfSelections': this.numberOfSelections,
            'countingCircles': this.countingCircles
          }
        ).then(response => {
          response.json().then((data) => {
            // success callback
            this.$toasted.success(this.$i18n.t('ElectionAdmin.successfully_set_up_election'))
          })
        }).catch(e => {
          this.$toasted.error(e.body.message)
        })
      }
    },
    startMixingPhase (newStatus) {
      this.$http.post('startMixingPhase',
        {
          'election': this.$route.params['electionId']
        }
      ).then(response => {
        response.json().then((data) => {
          this.$toasted.success(this.$i18n.t('ElectionAdmin.seccessfully_set_mixing_phase'))
        })
      }).catch(e => {
        this.$toasted.error(e.body.message)
      })
    },
    clear () {
      this.$refs.form.reset()
    },
    startDecryptionPhase (newStatus) {
      this.$http.post('startDecryptionPhase',
        {
          'election': this.$route.params['electionId']
        }
      ).then(response => {
        response.json().then((data) => {
          this.$toasted.success(this.$i18n.t('ElectionAdmin.successfully_set_mixing_phase'))
        })
      }).catch(e => {
        this.$toasted.error(e.body.message)
      })
    },

    tally () {
      this.$http.post('tally',
        {
          'election': this.$route.params['electionId']
        }
      ).then(response => {
        response.json().then((data) => {
          this.$toasted.success(this.$i18n.t('ElectionAdmin.successfully_tallied_election'))
        })
      }).catch(e => {
        this.$toasted.error(e.body.message)
      })
    }
  }
}
</script>
