<template>
    <v-container grid-list-md>
        <div v-if="this.$store.state.loaded">
            <ContentTitle icon="mdi-account-key" :title="$t('ElectionAdmin.title')"></ContentTitle>

            <div v-if="status == 0">
                <v-form v-model="valid" ref="form" lazy-validation >
                    <h5>Voters</h5>
                    <v-text-field :label="$t('number_of_voters')" v-model="numberOfVoters" required></v-text-field>
                    <v-text-field :label="$t('counting_circles')" v-model="countingCircles" required></v-text-field>
                    <div v-for="(election, index) in this.elections">
                        <h5>Election {{index+1}}</h5>
                        <v-text-field :label="$t('electionTitle')" v-model="election.title" required></v-text-field>
                        <v-text-field :label="$t('number_of_selections')" v-model="election.numberOfSelections" required></v-text-field>
                        <p>Candidates:</p>
                        <ul>
                            <li v-for="(c, ci) in election.candidates">
                                {{ci+1 }}. {{c}} <v-btn icon flat color="red" @click="election.candidates.splice(ci,1)"><v-icon>mdi-minus</v-icon></v-btn>
                            </li>
                        </ul>
                        <v-layout row wrap>
                            <v-flex xs6>
                            <v-text-field label="Candidate Name" v-model="election.newCandidateName"></v-text-field>
                            </v-flex>
                            <v-flex xs6>
                                <v-btn flat @click="election.candidates.push(election.newCandidateName); election.newCandidateName = ''"><v-icon>mdi-account-plus</v-icon> Add candidate</v-btn>
                            </v-flex>
                        </v-layout>
                    </div>
                    <v-btn @click="addElection()">Add election</v-btn>

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
                <p v-t="'ElectionAdmin.waitForMixing'"></p><br>
                <v-btn :disabled="!allAuthoritiesHaveMixed" @click="startDecryptionPhase()">{{ $t('ElectionAdmin.start_decryption_process') }}</v-btn>
            </div>
            <div v-if="status == 5">
                <p v-t="'ElectionAdmin.waitForDecryption'"></p>
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
                    <v-flex xy12 md12>
                        <DataCard :title="$t('final_results')" :expandable=false confidentiality="public">
                        <v-layout row wrap >
                            <v-flex xy12 md6 v-for="(results, index) in finalResults">
                            <donut-chart
                                    :id="`donut${index}`"
                                    :data="donutData[index]"
                                    colors='[ "#FF6384", "#36A2EB", "#FFCE56" ]'
                                    resize="false">
                            </donut-chart>
                            </v-flex>
                        </v-layout>

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
import Election from '../../models/election.js'
import VTextField from 'vuetify/es5/components/VTextField/VTextField'
import Vue from 'vue'

export default {
  components: {VTextField},
  mixins: [joinRoomMixin],
  data: () => ({
    valid: true,
    // candidates: '["Yes", "No", "Maybe"]',
    numberOfVoters: '5',
    newCandidateName: '',
    // numberOfSelections: '[1]',
    // numberOfCandidates: '[3]',
    countingCircles: '[1,1,1,1,1]',
    elections: [new Election()]
  }),
  computed: {
    ...mapGetters({
      electionId: 'electionId',
      status: 'status',
      allAuthoritiesHaveMixed: 'haveAllAuthoritiesMixed'
    }),
    ...mapState({
      votes: state => state.ElectionAdministrator.votes,
      w_bold: state => state.ElectionAdministrator.w_bold,
      finalResults: state => state.ElectionAdministrator.finalResults,
      electionCandidates: state => state.BulletinBoard.candidates,
      calcNumberOfCandidates: state => state.BulletinBoard.numberOfCandidates
    }),
    donutData: {
      get: function () {
        let donutData = []
        let candidateOffset = 0
        // loop over all parallel election events
        for (let i in this.finalResults) {
          let electionChartData = []
          for (let resIndex in this.finalResults[i]) {
            electionChartData.push({
              label: this.electionCandidates[Number(resIndex) + candidateOffset], value: this.finalResults[i][Number(resIndex)]
            })
          }
          candidateOffset = candidateOffset + this.calcNumberOfCandidates[i]
          donutData.push(electionChartData)
        }
        return donutData
      }
    }
  },
  methods: {
    addElection () {
      this.elections.push(new Election())
    },
    setUpElection (event) {
      if (this.$refs.form.validate()) {
        let candidates = Vue._.flatMap(this.elections, (election) => {
          return election.candidates
        })
        let numberOfCandidates = Vue._.flatMap(this.elections, (election) => {
          return election.candidates.length
        })
        let numberOfSelections = Vue._.flatMap(this.elections, (election) => {
          return election.numberOfSelections
        })

        this.$http.post('setUpElection',
          {
            'election': this.$route.params['electionId'],
            'numberOfVoters': this.numberOfVoters,
            'candidates': candidates,
            'numberOfCandidates': numberOfCandidates,
            'numberOfSelections': numberOfSelections,
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
      this.elections = [new Election()]
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
