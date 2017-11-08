<template>
    <v-container grid-list-md>
        <div v-if="this.$store.state.loaded">
            <ContentTitle icon="mdi-account-key" title="Election Administration"></ContentTitle>

            <div v-if="status == 0">
                <v-form v-model="valid" ref="form" lazy-validation>
                    <v-text-field
                            label="Candidates"
                            v-model="candidates"
                            required
                    ></v-text-field>
                    <v-text-field
                            label="Number of voters"
                            v-model="numberOfVoters"
                            required
                    ></v-text-field>
                    <v-text-field
                            label="Number of Candidates"
                            v-model="numberOfCandidates"
                            required
                    ></v-text-field>
                    <v-text-field
                            label="Number of selections"
                            v-model="numberOfSelections"
                            required
                    ></v-text-field>
                    <v-text-field
                            label="Counting Circles"
                            v-model="countingCircles"
                            required
                    ></v-text-field>

                    <v-btn color="primary" v-on:click="setUpElection" :disabled="!valid">setUpElection</v-btn>
                    <v-btn @click="clear">clear</v-btn>
                </v-form>
            </div>

            <div v-if="status == 1 || status == 2">
                The electorate data has been submitted to the printing authority.
            </div>

            <div v-if="status == 3">
                <v-btn @click="startMixingPhase()">End Election-Phase & start mixing process</v-btn>
            </div>

            <div v-if="status == 4">
                <v-btn @click="startDecryptionPhase()">Start decryption process</v-btn>
            </div>

            <div v-if="status == 6">
                <v-btn @click="tally()">Tally</v-btn>

                <h5>Post-Election data</h5>
                <v-layout row wrap>
                    <v-flex xy12 md4>
                        <DataCard title="Votes" :expandable=false confidentiality="public">{{votes}}
                        </DataCard>
                    </v-flex>
                    <v-flex xy12 md4>
                        <DataCard title="Final Results" :expandable=false confidentiality="public">{{finalResults}}
                        </DataCard>
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
            this.$toasted.success('Successfully set up election')
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
          this.$toasted.success('Successfully set election status to "Mixing Phase"')
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
          this.$toasted.success('Successfully set election status to "Mixing Phase"')
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
          this.$toasted.success('Successfully tallied election"')
        })
      }).catch(e => {
        this.$toasted.error(e.body.message)
      })
    }
  }
}
</script>
