<template>
    <transition-group tag="div" name="bounce" :appear="checkTransition">
        <v-layout row v-for="checkBallotTask in checkBallotTasks" :key="checkBallotTask.voterId">
            <v-flex xs12 sm12>
                <v-card>
                    <v-card-title primary-title>
                        <div>
                            <div class="headline">Ballot check for voter {{checkBallotTask.voterId + 1}}</div>
                        </div>
                    </v-card-title>
                    <v-card-text>
                        <p>Please check the ballot and respond to the query</p>
                    </v-card-text>
                    <v-card-text v-if="checkBallotTask.checkResults[selectedAuthorityIndex] != null">
                        Result of Check: {{ checkBallotTask.checkResults[selectedAuthorityIndex] }}
                    </v-card-text>
                    <v-card-actions>
                        <v-btn flat color="blue" @click="checkBallot(checkBallotTask.voterId)">
                            <v-icon left>mdi-approval</v-icon>
                            Check Validity
                        </v-btn>
                        <v-btn flat color="blue" @click="respond(checkBallotTask.voterId)"
                               :disabled="!checkBallotTask.checkResults[selectedAuthorityIndex]">
                            <v-icon left>mdi-reply</v-icon>
                            Respond to query
                        </v-btn>
                        <v-btn flat color="red" @click="discardBallot(checkBallotTask.voterId)"
                               :disabled="checkBallotTask.checkResults[selectedAuthorityIndex] || checkBallotTask.checkResults[selectedAuthorityIndex] == null">
                            <v-icon left>mdi-cancel</v-icon>
                            Discard ballot
                        </v-btn>
                        <v-spacer></v-spacer>
                        <v-btn icon @click.native="show = !show">
                            <v-icon>{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
                        </v-btn>
                    </v-card-actions>
                    <v-slide-y-transition>
                        <v-card-text v-show="show">
                            a_bold: {{ checkBallotTask.ballot.a_bold }}<br>
                            x_hat: {{ checkBallotTask.ballot.x_hat }}
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
        checkBallot: function (voterId) {
          this.$http.post('checkVote', {
            'election': this.$route.params['electionId'],
            'authorityId': this.selectedAuthorityIndex,
            'voterId': voterId
          }).then(response => {
            response.json().then((data) => {
              // success callback
              this.$toasted.success('Successfully checked vote')
            })
          }).catch(e => {
            this.$toasted.error(e.body.message)
          })
        },
        respond: function (voterId) {
          this.$http.post('respond', {
            'election': this.$route.params['electionId'],
            'authorityId': this.selectedAuthorityIndex,
            'voterId': voterId
          }).then(response => {
            response.json().then((data) => {
              // success callback
              this.$toasted.success('Successfully replied to vote')
            })
          }).catch(e => {
            this.$toasted.error(e.body.message)
          })
        },
        discardBallot: function (voterId) {
          this.$http.post('discardBallot', {
            'election': this.$route.params['electionId'],
            'authorityId': this.selectedAuthorityIndex,
            'voterId': voterId
          }).then(response => {
            response.json().then((data) => {
              // success callback
              this.$toasted.success('Successfully replied to vote')
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
        animation: bounce-in .5s;
    }

    .bounce-leave-active {
        animation: bounce-in .4s reverse;
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