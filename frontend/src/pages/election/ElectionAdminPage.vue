<template>
  <v-container grid-list-md>
    <div v-if="this.$store.state.loaded">
      <ContentTitle icon="mdi-account-key" :title="$t('ElectionAdmin.title')">
        <v-menu offset-y v-if="status == 0">
          <v-btn color="primary" dark slot="activator">Election presets</v-btn>
          <v-list>
            <v-list-tile v-for="preset in electionPresets" :key="preset.title" @click="setElectionPreset(preset.generate())">
              <v-list-tile-title>{{ preset.title }}</v-list-tile-title>
            </v-list-tile>
          </v-list>
        </v-menu>
      </ContentTitle>

      <div v-if="status == 0">
        <v-form v-model="valid" ref="form" lazy-validation>
          <h5 v-t="'counting_circles'"></h5>
          <div v-for="(voters, index) in countingCircles">
            <v-layout row wrap>
              <v-flex xs6>
                <v-text-field label="Number of voters in this counting circle" type="number" v-model="countingCircles[index]" autofocus required></v-text-field>
              </v-flex>
              <v-flex xs6>
                <v-btn fab icon small dark color="error" title="Remove counting circle" v-if="index <= countingCircles.length && countingCircles.length > 1" @click="countingCircles.splice(index, 1)">
                  <v-icon>mdi-minus</v-icon>
                </v-btn>
                <v-btn fab icon small dark color="primary" title="Add counting circle" v-if="index === countingCircles.length - 1" @click="countingCircles.push(null)">
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
              </v-flex>
            </v-layout>
          </div>

          <div v-for="(election, index) in this.elections">
            <h5>
              Election {{ index + 1 }}
              <v-btn icon small dark color="error" title="Remove this election" v-if="index > 0" @click="elections.splice(index, 1)">
                <v-icon>mdi-minus</v-icon>
              </v-btn>
            </h5>
            <v-layout row wrap>
              <v-flex xs3>
                <v-text-field :label="$t('electionTitle')" v-model="election.title" autofocus required></v-text-field>
              </v-flex>
              <v-flex xs3>
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
            </v-layout>
          </div>

          <v-btn @click="addElection()">Add election</v-btn>
          <v-btn @click="setUpElection" color="primary" :disabled="!valid">{{ $t('ElectionAdmin.set_up_election') }}</v-btn>
          <v-btn @click="clear" color="error">{{ $t('clear') }}</v-btn>
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

      <div v-if="status >= 6">
        <v-btn v-if="finalResults.length === 0" @click="tally()">{{ $t('tally') }}</v-btn>
        <v-btn v-else @click="publishResult()">{{ $t('ElectionAdmin.publishResult') }}</v-btn>
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
    // numberOfSelections: '[1]',
    // numberOfCandidates: '[3]',
    countingCircles: [ 3 ],
    elections: [new Election()],
    electionPresets: [
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
          /*
          const candidates = [
            'Donald Trump', 'Vladimir Putin', 'George W Bush', 'Barack Obama', 'Hillary Clinton',
            'Vladimir Putin', 'Winston Churchill', 'Abraham Lincoln', 'Nelson Mandela', 'Otto von Bismarck',
            'Angela Merkel', 'Chuck Norris', 'David Hasselhoff', 'Helene Fischer', 'Michelle Obama',
            'Marine Le Pen', 'Tony Blair', 'Bill Clinton', 'Donald Rumsfeld', 'Condoleezza Rice'
          ]
          */
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
            return election
          })

          return this
        }
      }
    ]
  }),
  computed: {
    ...mapGetters({
      electionId: 'electionId',
      status: 'status',
      allAuthoritiesHaveMixed: 'haveAllAuthoritiesMixed'
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
    addElection () {
      this.elections.push(new Election())
    },
    removeCandidate (electionIndex, candidate) {
      this.elections[electionIndex].candidates.splice(this.elections[electionIndex].candidates.indexOf(candidate), 1)
      this.elections[electionIndex].candidates = [...this.elections[electionIndex].candidates]
    },
    setUpElection (event) {
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
