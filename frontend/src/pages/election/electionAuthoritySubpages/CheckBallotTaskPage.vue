<template>
    <transition-group tag="div" name="bounce" :appear="checkTransition">
        <v-layout row wrap v-for="checkBallotTask in checkBallotTasks" :key="checkBallotTask.ballotId">
            <v-flex xs12 sm12>
                <v-card>
                    <v-card-title primary-title>
                        <div>
                            <div class="headline">{{ $t('CheckBallotTask.ballot_check_for_voter_n', { n: checkBallotTask.voterId + 1 }) }}</div>
                        </div>
                    </v-card-title>
                    <v-card-text>
                        <p v-t="'CheckBallotTask.check_ballot_and_respond'"></p>
                    </v-card-text>
                    <v-card-text v-if="checkBallotTask.checkResults[selectedAuthorityIndex] != null">
                        <p>{{ $t('result_of_check') }}</p>:<b>
                            <p v-if="checkBallotTask.checkResults[selectedAuthorityIndex] === 0" v-t="'BallotList.unchecked'"></p>
                            <p v-if="checkBallotTask.checkResults[selectedAuthorityIndex] === 1" v-t="'BallotList.validBallot'"></p>
                            <p v-if="checkBallotTask.checkResults[selectedAuthorityIndex] === 2" v-t="'BallotList.ballotProofInvalid'"></p>
                            <p v-if="checkBallotTask.checkResults[selectedAuthorityIndex] === 3" v-t="'BallotList.alreadyHasBallot'"></p>
                            <p v-if="checkBallotTask.checkResults[selectedAuthorityIndex] === 4" v-t="'BallotList.credentialInvalid'"></p>
                            <p v-if="checkBallotTask.checkResults[selectedAuthorityIndex] === 5" v-t="'BallotList.queryInvalid'"></p>
                        </b>

                    </v-card-text>
                    <v-card-actions>
                        <v-btn flat color="blue" @click="checkBallot(checkBallotTask.ballotId)" :disabled="checkBallotTask.checkResults[selectedAuthorityIndex] != null">
                            <v-icon left>mdi-approval</v-icon>
                            {{ $t('check_validity') }}
                        </v-btn>
                        <v-btn flat color="blue" @click="respond(checkBallotTask.ballotId)"
                               :disabled="checkBallotTask.checkResults[selectedAuthorityIndex] !== 1">
                            <v-icon left>mdi-reply</v-icon>
                            {{ $t('CheckBallotTask.respond_to_query') }}
                        </v-btn>
                        <v-btn flat color="red" @click="discardBallot(checkBallotTask.ballotId)"
                               :disabled="checkBallotTask.checkResults[selectedAuthorityIndex] == 1 || checkBallotTask.checkResults[selectedAuthorityIndex] == null">
                            <v-icon left>mdi-cancel</v-icon>
                            {{ $t('CheckBallotTask.discard_ballot') }}
                        </v-btn>
                        <v-spacer></v-spacer>
                        <v-btn icon @click.native="show = !show">
                            <v-icon>{{ !show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
                        </v-btn>
                    </v-card-actions>
                    <v-slide-y-transition>
                        <v-card-text v-show="show">
                            <div v-for="ballot in getBallotById(checkBallotTask.ballotId)">
                                <v-card>
                                    <v-card-text class="grey lighten-3">
                                        <v-layout row wrap>
                                            <v-flex xy2 md2 v-t="'ElectionAuthority.encrypted_selections'"></v-flex>
                                            <v-flex x10 md10>
                                <span v-for="(elgamalEncryption, i) in ballot.ballot.a_bold">
                                  (<BigIntLabel :mpzValue="elgamalEncryption[0]"></BigIntLabel>,
                                  <BigIntLabel :mpzValue="elgamalEncryption[1]"></BigIntLabel>)<span v-if="i < ballot.ballot.a_bold.length - 1">, </span>
                                </span>
                                            </v-flex>
                                        </v-layout>
                                        <v-layout row wrap>
                                            <v-flex xy2 md2 v-t="'ElectionAuthority.public_voter_credential'"></v-flex>
                                            <v-flex xy10 md10>
                                                <BigIntLabel :mpzValue="ballot.ballot.x_hat"></BigIntLabel>
                                            </v-flex>
                                        </v-layout>
                                        <v-layout row wrap>
                                            <v-flex xy2 md2 v-t="'ElectionAuthority.ballot_proof'"></v-flex>
                                            <v-flex x10 md10>
                                                (<BigIntLabel :mpzValue="ballot.ballot.pi[0][0]"></BigIntLabel>,
                                                <BigIntLabel :mpzValue="ballot.ballot.pi[0][1]"></BigIntLabel>,
                                                <BigIntLabel :mpzValue="ballot.ballot.pi[0][2]"></BigIntLabel>),
                                                (<BigIntLabel :mpzValue="ballot.ballot.pi[1][0]"></BigIntLabel>,
                                                <BigIntLabel :mpzValue="ballot.ballot.pi[1][1]"></BigIntLabel>,
                                                <BigIntLabel :mpzValue="ballot.ballot.pi[1][2]"></BigIntLabel>)
                                            </v-flex>
                                        </v-layout>
                                    </v-card-text>
                                </v-card>
                            </div>
                        </v-card-text>
                    </v-slide-y-transition>
                </v-card>
            </v-flex>
        </v-layout>
    </transition-group>
</template>

<script>
    export default {
      data: () => ({
        show: false,
        checkTransition: false
      }),
      mounted () {
        this.checkTransition = false
      },
      computed: {
        selectedAuthorityIndex: {
          get: function () {
            return parseInt(this.$route.params.authid)
          },
          set: function (newAuthId) {
            this.$store.commit('selectedAuthority', newAuthId)
            this.$router.push({name: 'electionauthority', params: {electionId: this.$route.params['electionId'], authid: newAuthId}})
          }
        },
        electionAuthority: {
          get: function () {
            return this.$store.getters.getElectionAuthority(this.selectedAuthorityIndex)
          }
        },
        checkBallotTasks: {
          get: function () {
            return this.$store.getters.getCheckBallotTasks(this.selectedAuthorityIndex)
          }
        }
      },
      methods: {
        getBallotById: function (id) {
          return this.$store.getters.getBallotById(id)
        },
        checkBallot: function (ballotId) {
          this.$http.post('checkVote', {
            'election': this.$route.params['electionId'],
            'authorityId': this.selectedAuthorityIndex,
            'ballotId': ballotId
          }).then(response => {
            response.json().then((data) => {
              // success callback
              this.$toasted.success(this.$i18n.t('CheckBallotTask.successfully_checked_vote'))
            })
          }).catch(e => {
            this.$toasted.error(e.body.message)
          })
        },
        respond: function (ballotId) {
          this.$http.post('respond', {
            'election': this.$route.params['electionId'],
            'authorityId': this.selectedAuthorityIndex,
            'ballotId': ballotId
          }).then(response => {
            response.json().then((data) => {
              // success callback
              this.$toasted.success(this.$i18n.t('CheckBallotTask.successfully_replied_to_vote'))
            })
          }).catch(e => {
            this.$toasted.error(e.body.message)
          })
        },
        discardBallot: function (ballotId) {
          this.$http.post('discardBallot', {
            'election': this.$route.params['electionId'],
            'authorityId': this.selectedAuthorityIndex,
            'ballotId': ballotId
          }).then(response => {
            response.json().then((data) => {
              // success callback
              // this.$toasted.success(this.$i18n.t('CheckBallotTask.successfully_replied_to_vote'))
            })
          }).catch(e => {
            this.$toasted.error(e.body.message)
          })
        }
      }
    }
</script>

<style>

</style>
