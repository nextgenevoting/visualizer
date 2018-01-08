<template>
    <transition-group tag="div" name="bounce" :appear="checkTransition">
        <v-layout row wrap v-for="checkConfirmationTask in checkConfirmationTasks"
                  :key="checkConfirmationTask.confirmationId">
            <v-flex xs12 sm12>
                <v-card>
                    <v-card-title primary-title>
                        <div>
                            <div class="headline">
                                {{ $t('ConfirmationTask.confirmation_for_voter_n', {n: checkConfirmationTask.voterId + 1})
                                }}
                            </div>
                        </div>
                    </v-card-title>
                    <v-card-text>
                        <p v-t="'ConfirmationTask.check_confirmation_and_finalize'"></p>
                    </v-card-text>
                    <v-card-text v-if="checkConfirmationTask.checkResults[selectedAuthorityIndex] != null">
                        <p>{{ $t('result_of_check') }}</p>:<b>
                        <p v-if="checkConfirmationTask.checkResults[selectedAuthorityIndex] === 0"
                           v-t="'BallotList.unchecked'"></p>
                        <p v-if="checkConfirmationTask.checkResults[selectedAuthorityIndex] === 1"
                           v-t="'BallotList.valid'"></p>
                        <p v-if="checkConfirmationTask.checkResults[selectedAuthorityIndex] === 2"
                           v-t="'BallotList.ballotProofInvalid'"></p>
                        <p v-if="checkConfirmationTask.checkResults[selectedAuthorityIndex] === 3"
                           v-t="'BallotList.confirmationHasNoBallot'"></p>
                        <p v-if="checkConfirmationTask.checkResults[selectedAuthorityIndex] === 4"
                           v-t="'BallotList.alreadyHasConfirmation'"></p>
                        <p v-if="checkConfirmationTask.checkResults[selectedAuthorityIndex] === 5"
                           v-t="'BallotList.credentialInvalid'"></p>
                    </b>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn flat color="blue" @click="checkConfirmation(checkConfirmationTask.confirmationId)"
                               :disabled="checkConfirmationTask.checkResults[selectedAuthorityIndex] != null">
                            <v-icon left>mdi-approval</v-icon>
                            {{ $t('check_validity') }}
                        </v-btn>
                        <v-btn flat color="blue" @click="finalize(checkConfirmationTask.confirmationId)"
                               :disabled="checkConfirmationTask.checkResults[selectedAuthorityIndex] !== 1">
                            <v-icon left>mdi-reply</v-icon>
                            {{ $t('finalize') }}
                        </v-btn>
                        <v-btn flat color="red" @click="discardConfirmation(checkConfirmationTask.confirmationId)"
                               :disabled="checkConfirmationTask.checkResults[selectedAuthorityIndex] == 1 || checkConfirmationTask.checkResults[selectedAuthorityIndex] == null">
                            <v-icon left>mdi-cancel</v-icon>
                            {{ $t('ConfirmationTask.discard_confirmation') }}
                        </v-btn>
                        <v-spacer></v-spacer>
                        <v-btn icon @click.native="show = !show">
                            <v-icon>{{ !show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
                        </v-btn>
                    </v-card-actions>
                    <v-slide-y-transition>
                        <v-card-text v-show="show">
                            <div v-for="confirmation in getConfirmationById(checkConfirmationTask.confirmationId)">
                                <v-card>
                                    <v-card-text class="grey lighten-3">

                                        <v-layout row wrap>
                                            <v-flex xy3 md3 v-t="'ElectionAuthority.public_confirmation_credential'"></v-flex>
                                            <v-flex xy9 md9>
                                                <BigIntLabel :mpzValue="confirmation.confirmation.y_hat"></BigIntLabel>
                                            </v-flex>
                                        </v-layout>
                                        <v-layout row wrap>
                                            <v-flex xy3 md3 v-t="'ElectionAuthority.confirmation_proof'"></v-flex>
                                            <v-flex xy9 md9>
                                                (
                                                <BigIntLabel :mpzValue="confirmation.confirmation.pi[0]"></BigIntLabel>
                                                ,
                                                <BigIntLabel :mpzValue="confirmation.confirmation.pi[1]"></BigIntLabel>
                                                )
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
            this.$router.push({
              name: 'electionauthority',
              params: {electionId: this.$route.params['electionId'], authid: newAuthId}
            })
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
        getConfirmationById: function (id) {
          return this.$store.getters.getConfirmationById(id)
        },
        checkConfirmation: function (confirmationId) {
          this.$http.post('checkConfirmation', {
            'election': this.$route.params['electionId'],
            'authorityId': this.selectedAuthorityIndex,
            'confirmationId': confirmationId
          }).then(response => {
            response.json().then((data) => {
              // success callback
              this.$toasted.success(this.$i18n.t('ConfirmationTask.successfully_checked_confirmation'))
            })
          }).catch(e => {
            this.$toasted.error(e.body.message)
          })
        },
        finalize: function (confirmationId) {
          this.$http.post('finalize', {
            'election': this.$route.params['electionId'],
            'authorityId': this.selectedAuthorityIndex,
            'confirmationId': confirmationId
          }).then(response => {
            response.json().then((data) => {
              // success callback
              this.$toasted.success(this.$i18n.t('ConfirmationTask.successfully_finalized_ballot'))
            })
          }).catch(e => {
            this.$toasted.error(e.body.message)
          })
        },
        discardConfirmation: function (confirmationId) {
          this.$http.post('discardConfirmation', {
            'election': this.$route.params['electionId'],
            'authorityId': this.selectedAuthorityIndex,
            'confirmationId': confirmationId
          }).then(response => {
            response.json().then((data) => {
              // success callback
              this.$toasted.success(this.$i18n.t('ConfirmationTask.successfully_discarded_confirmation'))
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
