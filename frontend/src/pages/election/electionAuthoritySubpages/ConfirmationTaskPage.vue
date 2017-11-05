<template>
    <transition-group tag="div" name="bounce" :appear="checkTransition">
        <v-layout row v-for="checkConfirmationTask in checkConfirmationTasks" :key="checkConfirmationTask.voterId">
            <v-flex xs12 sm12>
                <v-card>
                    <v-card-title primary-title>
                        <div>
                            <div class="headline">Confirmation for voter {{checkConfirmationTask.voterId + 1}}</div>
                        </div>
                    </v-card-title>
                    <v-card-text>
                        <p>Please check the confirmation and finalize the vote</p>
                    </v-card-text>
                    <v-card-text v-if="checkConfirmationTask.checkResults[selectedAuthorityIndex] != null">
                        Result of Check: {{ checkConfirmationTask.checkResults[selectedAuthorityIndex] }}
                    </v-card-text>
                    <v-card-actions>
                        <v-btn flat color="blue" @click="checkConfirmation(checkConfirmationTask.voterId)">
                            <v-icon left>mdi-approval</v-icon>
                            Check Validity
                        </v-btn>
                        <v-btn flat color="blue" @click="finalize(checkConfirmationTask.voterId)"
                               :disabled="!checkConfirmationTask.checkResults[selectedAuthorityIndex]">
                            <v-icon left>mdi-reply</v-icon>
                            Finalize
                        </v-btn>
                        <v-btn flat color="red" @click="discardConfirmation(checkConfirmationTask.voterId)"
                               :disabled="checkConfirmationTask.checkResults[selectedAuthorityIndex] || checkConfirmationTask.checkResults[selectedAuthorityIndex] == null">
                            <v-icon left>mdi-cancel</v-icon>
                            Discard confirmation
                        </v-btn>
                        <v-spacer></v-spacer>
                        <v-btn icon @click.native="show = !show">
                            <v-icon>{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
                        </v-btn>
                    </v-card-actions>
                    <v-slide-y-transition>
                        <v-card-text v-show="show">
                            todo: infos about the confirmation
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
        checkConfirmationTasks: {
          get: function () {
            return this.$store.getters.getCheckConfirmationTasks(this.selectedAuthorityIndex)
          }
        }
      },
      methods: {
        checkConfirmation: function (voterId) {
          this.$http.post('checkConfirmation', {
            'election': this.$route.params['electionId'],
            'authorityId': this.selectedAuthorityIndex,
            'voterId': voterId
          }).then(response => {
            response.json().then((data) => {
              // success callback
              this.$toasted.success('Successfully checked confirmation')
            })
          }).catch(e => {
            this.$toasted.error(e.body.message)
          })
        },
        finalize: function (voterId) {
          this.$http.post('finalize', {
            'election': this.$route.params['electionId'],
            'authorityId': this.selectedAuthorityIndex,
            'voterId': voterId
          }).then(response => {
            response.json().then((data) => {
              // success callback
              this.$toasted.success('Successfully finalized ballot')
            })
          }).catch(e => {
            this.$toasted.error(e.body.message)
          })
        },
        discardConfirmation: function (voterId) {
          this.$http.post('discardConfirmation', {
            'election': this.$route.params['electionId'],
            'authorityId': this.selectedAuthorityIndex,
            'voterId': voterId
          }).then(response => {
            response.json().then((data) => {
              // success callback
              this.$toasted.success('Successfully discarded confirmation')
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