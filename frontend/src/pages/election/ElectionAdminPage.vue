<template>
  <v-container grid-list-md :fluid="fluidLayout">
    <div v-if="this.$store.state.loaded">
      <ContentTitle customicon="customicon icon-election-administrator" :title="$t('ElectionAdmin.title')">
        <v-menu offset-y v-if="status == 0">
          <v-btn slot="activator">{{ $t('ElectionAdmin.election_presets') }}</v-btn>
          <v-list>
            <v-list-tile v-for="preset in electionPresets" :key="preset.title" @click="setElectionPreset(preset.generate())">
              <v-list-tile-title>{{ preset.title }}</v-list-tile-title>
            </v-list-tile>
          </v-list>
        </v-menu>
      </ContentTitle>

      <!--v-flex xs12 sm1>
        <h5 v-t="'tasks'"></h5>
      </v-flex-->

      <v-alert v-if="status == 1 || status == 2" color="grey lighten-3" icon="info" value="true">
        {{ $t('ElectionAdmin.submitted_to_printing_authority') }}
      </v-alert>
      <v-alert v-if="status == 4 && !allAuthoritiesHaveMixed" color="grey lighten-3" icon="info" value="true">
        {{ $t('ElectionAdmin.waitForMixing') }}
      </v-alert>
      <v-alert v-if="status == 5 && !haveAllAuthoritiesDecrypted" color="grey lighten-3" icon="info" value="true">
        {{ $t('ElectionAdmin.waitForDecryption') }}
      </v-alert>

      <v-flex x12 md12 v-if="status == 0">
        <v-card style="margin-bottom: 20px;">
          <v-card-title primary-title>
            <div class="headline" v-t="'ElectionAdmin.set_up_election'"></div>
          </v-card-title>
          <v-card-text>
            <v-form v-model="valid" ref="form" lazy-validation>
              <h5>{{$t('counting_circles')}} <v-tooltip top>
                <v-icon  color="grey lighten-1" slot="activator">info</v-icon><span>{{$t('ElectionAdmin.counting_circles_tooltip')}}</span>
              </v-tooltip></h5>

              <div v-for="(voters, index) in countingCircles">
                <v-layout row wrap>
                  <v-flex xs6>
                    <v-text-field :label="$t('ElectionAdmin.number_of_voters')" type="number" v-model="countingCircles[index]" autofocus required></v-text-field>
                  </v-flex>
                  <v-flex xs6>
                    <v-btn fab icon small title="Remove counting circle" v-if="index <= countingCircles.length && countingCircles.length > 1" @click="countingCircles.splice(index, 1)">
                      <v-icon color="error">mdi-close</v-icon>
                    </v-btn>
                    <v-btn fab icon small  title="Add counting circle" v-if="index === countingCircles.length - 1" @click="countingCircles.push(null)">
                      <v-icon>mdi-plus</v-icon>
                    </v-btn>
                  </v-flex>
                </v-layout>
              </div>

              <div v-for="(election, index) in this.elections">
                <h5>
                  {{$t('election')}} {{ index + 1 }}
                  <v-btn icon small flat color="error" title="Remove this election" v-if="index > 0" @click="elections.splice(index, 1)">
                    <v-icon>mdi-close-circle</v-icon>
                  </v-btn>
                </h5>

                <v-layout row wrap>
                  <v-flex xs12 md12>
                    <v-text-field :label="$t('electionTitle')" v-model="election.title" autofocus required></v-text-field>
                  </v-flex>
                </v-layout>
                <v-layout row wrap>
                  <v-flex xs6 md6>
                    <v-text-field type="number" :label="$t('number_of_selections')" v-model="election.numberOfSelections" required></v-text-field>
                  </v-flex>
                </v-layout>
                <v-layout row wrap>
                  <v-flex xs6>
                    <v-select flat chips tags required append-icon="" label="Candidates (hit TAB to add a candidate)" v-model="election.candidates">
                      <template slot="selection" slot-scope="data">
                        <v-chip close @input="removeCandidate(index, data.item)" :selected="data.selected">
                          <b>{{ data.item }}</b>
                        </v-chip>
                      </template>
                    </v-select>
                  </v-flex>
                  <v-flex xs2>
                    <v-menu offset-y v-if="status == 0">
                      <v-btn slot="activator">{{ $t('ElectionAdmin.candidate_presets') }}</v-btn>
                      <v-list>
                        <v-list-tile v-for="preset in candidatePresets" :key="preset.title" @click="setCandidatePreset(election, preset.generate())">
                          <v-list-tile-title>{{ preset.title }}</v-list-tile-title>
                        </v-list-tile>
                      </v-list>
                    </v-menu>
                  </v-flex>
                </v-layout>
              </div>

              <v-btn @click="addElection()">{{ $t('ElectionAdmin.add_election') }}</v-btn>
              <v-btn @click="setUpElection" color="primary" :disabled="!valid">{{ $t('ElectionAdmin.set_up_election') }}</v-btn>
              <v-btn @click="clear" color="error">{{ $t('clear') }}</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-flex>


      <v-btn :disabled="status != 3" @click="startMixingPhase()">{{ $t('ElectionAdmin.end_election_phase') }}</v-btn>
      <v-btn :disabled="!(allAuthoritiesHaveMixed && status == 4)" @click="startDecryptionPhase()">{{ $t('ElectionAdmin.start_decryption_process') }}</v-btn>
      <v-btn :disabled="!(haveAllAuthoritiesDecrypted && finalResults.length === 0 && status === 6)" @click="tally()">{{ $t('tally') }}</v-btn>
      <v-btn :disabled="!(status === 6 && finalResults.length > 0)" @click="publishResult()">{{ $t('ElectionAdmin.publishResult') }}</v-btn>

      <div v-if="status >= 6" style="margin-top:15px;">
        <h5 v-t="'post_election_data'"></h5>
        <ElectionResult></ElectionResult>
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

const rand = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min

export default {
  components: {VTextField},
  mixins: [joinRoomMixin],
  data: () => ({
    valid: false,
    candidates: [],
    countingCircles: [ 3 ],
    elections: [new Election()],
    electionPresets: [
      { title: 'Demo',
        generate: () => {
          let election = new Election()
          election.title = 'Welchem Abgeordneten geben Sie Ihre Stimme?'
          election.candidates = [ 'Dominik Vogel', 'Johanna Frei', 'Markus Kohl' ]
          election.numberOfSelections = 1
          this.countingCircles = [ 3 ]
          this.elections = [ election ]
          return this
        }
      },
      { title: '3 counting circles',
        generate: () => {
          let election = new Election()
          election.candidates = [ 'Yes', 'No', 'Blank' ]
          this.countingCircles = [ 2, 2, 3 ]
          this.elections = [ election ]
          return this
        }
      },
      { title: 'Random election',
        generate: () => {
          const candidates = [
            'Soila', 'Sheryll', 'Shawnna', 'Regena', 'Lien', 'Wynell', 'Erna', 'Lesia', 'Cordia', 'Pattie',
            'Susie', 'Annmarie', 'Argentina', 'Herminia', 'Leeanna', 'Audrey', 'Sherilyn', 'Verdell', 'Denita',
            'Tara', 'Wilton', 'Thanh', 'Mitchel', 'Romeo', 'Vern', 'Thad', 'Willard', 'Bryon', 'Jacinto', 'Kelvin',
            'Carmine', 'Mervin', 'Benjamin', 'Fidel', 'Isreal', 'Carmen', 'Ulysses', 'Fredric', 'Rob', 'Britt'
          ]

          this.countingCircles = [...new Array(rand(1, 5))].map(() => rand(2, 5))
          this.elections = [...new Array(rand(1, 4))].map(() => {
            let election = new Election()
            let c = candidates
            election.candidates = [...new Array(rand(2, 5))].map(() => c.splice(c, 1)[0])
            election.numberOfSelections = Math.max(1, rand(1, election.candidates.length - 1))
            return election
          })

          return this
        }
      }
    ],
    candidatePresets: [
      { title: 'Yes, No, Blank',
        generate: () => {
          return [ 'Yes', 'No', 'Blank' ]
        }
      }
    ]
  }),
  computed: {
    ...mapGetters({
      electionId: 'electionId',
      status: 'status',
      allAuthoritiesHaveMixed: 'haveAllAuthoritiesMixed',
      haveAllAuthoritiesDecrypted: 'haveAllAuthoritiesDecrypted',
      fluidLayout: 'fluidLayout'
    }),
    ...mapState({
      finalResults: state => state.ElectionAdministrator.finalResults
    })
  },
  methods: {
    setElectionPreset (preset) {
      this.countingCircles = preset.countingCircles
      this.elections = preset.elections
    },
    setCandidatePreset (election, preset) {
      election.candidates = preset
    },
    addElection () {
      this.elections.push(new Election())
    },
    removeCandidate (electionIndex, candidate) {
      this.elections[electionIndex].candidates.splice(this.elections[electionIndex].candidates.indexOf(candidate), 1)
      this.elections[electionIndex].candidates = [...this.elections[electionIndex].candidates]
    },
    setUpElection () {
      if (this.$refs.form.validate()) {
        let numberOfVoters = this.countingCircles.reduce((a, b) => parseInt(a) + parseInt(b), 0).toString()
        let candidates = Vue._.flatMap(this.elections, (election) => election.candidates)
        let numberOfCandidates = Vue._.flatMap(this.elections, (election) => election.candidates.length)
        let numberOfSelections = Vue._.flatMap(this.elections, (election) => parseInt(election.numberOfSelections))
        let titles = Vue._.flatMap(this.elections, (election) => election.title)
        let countingCircles = (() => {
          var i = 1
          return JSON.stringify(Vue._.flatMap(this.countingCircles.map((n) => Array(parseInt(n)).fill(i++))))
        })()

        this.$http.post('setUpElection', {
          'election': this.$route.params['electionId'],
          'numberOfVoters': numberOfVoters,
          'candidates': candidates,
          'numberOfCandidates': numberOfCandidates,
          'numberOfSelections': numberOfSelections,
          'countingCircles': countingCircles,
          'titles': titles
        }).then(response => {
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
      this.$http.post('startMixingPhase', { 'election': this.$route.params['electionId'] }).then(response => {
        response.json().then((data) => {
          this.$toasted.success(this.$i18n.t('ElectionAdmin.successfully_set_mixing_phase'))
        })
      }).catch(e => {
        this.$toasted.error(e.body.message)
      })
    },
    clear () {
      this.$refs.form.reset()
      this.countingCircles = [ 3 ]
      this.elections = [ new Election() ]
    },
    startDecryptionPhase (newStatus) {
      this.$http.post('startDecryptionPhase',
        {
          'election': this.$route.params['electionId']
        }
      ).then(response => {
        response.json().then((data) => {
          this.$toasted.success(this.$i18n.t('ElectionAdmin.successfully_set_decryption_phase'))
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
    },
    publishResult () {
      this.$http.post('publishResult',
        {
          'election': this.$route.params['electionId']
        }
      ).then(response => {
        response.json().then((data) => {
          this.$toasted.success(this.$i18n.t('ElectionAdmin.successfully_published_result'))
        })
      }).catch(e => {
        this.$toasted.error(e.body.message)
      })
    }
  }
}
</script>
