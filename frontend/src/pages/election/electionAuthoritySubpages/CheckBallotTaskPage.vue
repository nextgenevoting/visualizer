<template>
    <transition-group tag="div" name="bounce" :appear="checkTransition">
        <v-layout row v-for="checkBallotTask in checkBallotTasks" :key="checkBallotTask.ballotId">
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
                        {{ $t('result_of_check') }}: {{ checkBallotTask.checkResults[selectedAuthorityIndex] }}
                    </v-card-text>
                    <v-card-actions>
                        <v-btn flat color="blue" @click="checkBallot(checkBallotTask.ballotId)">
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
                            <v-icon>{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
                        </v-btn>
                    </v-card-actions>
                    <v-slide-y-transition>
                        <v-card-text v-show="show">
                            <!--a_bold: {{ checkBallotTask.ballot.a_bold }}<br>
                            x_hat: {{ checkBallotTask.ballot.x_hat }}-->
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
    .bounce-enter-active {
        animation: bounce-in .8s;
    }

    .bounce-leave-active {
        animation: bounce-in .8s reverse;
    }

    @keyframes bounce-in {
        0% {
            transform: scale(0);
            opacity: 0;
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }
</style>