<template>
    <v-container grid-list-md>
        <div v-if="this.$store.state.loaded">
            <ContentTitle icon="mdi-settings-box" title="Election Authorities"></ContentTitle>
            <v-layout row>

                <v-flex xs12 sm12>
                    <v-btn-toggle v-model="selectedAuthorityIndex">
                        <v-btn flat v-for="auth in electionAuthorities">
                            <v-badge color="blue" right>
                                <span slot="badge" v-if="auth.checkBallotTasks.length > 0">{{ auth.checkBallotTasks.length
                                    }}</span>
                                <v-icon>mdi-settings-box</v-icon>
                                Authority {{auth.id + 1}}
                            </v-badge>
                        </v-btn>
                    </v-btn-toggle>
                </v-flex>
            </v-layout>
            <br>
            <v-layout row>
                <v-flex xs12 sm1><h5 class="">Tasks</h5></v-flex>
                <v-flex sm12 sm11>
                    <v-switch label="Automatic processing" v-model="autoMode"></v-switch>
                </v-flex>
            </v-layout>
            <transition-group tag="div" :name="checkTransitionClass" :appear="checkTransition">
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

            <transition-group tag="div" :name="checkTransitionClass" :appear="checkTransition">
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

            <h5 class="">Data</h5>

            <v-layout row wrap>

                <v-flex xy12 md12>
                    <DataCard title="Ballots" :isMpz=true :expandable=false confidentiality="encrypted">

                        <transition-group tag="v-expansion-panel" :name="ballotTransitionClass" class="expansion-panel--popout" :appear="ballotTransition">
                            <v-expansion-panel-content v-for="ballot in ballots" :key="ballot.ballot.x_hat">
                                <div slot="header">Ballot of voter {{ballot.voterId}}
                                    <transition :name="ballotTransitionClass">
                                        <v-chip left label outline color="green" v-if="ballot.confirmation !== null">Confirmed</v-chip>
                                    </transition>
                                </div>
                                <v-card>
                                    <v-card-text class="grey lighten-3">
                                        <v-layout row>
                                            <v-flex xy4 md4>Encrypted selections / queries:</v-flex>
                                            <v-flex xy8 md8>
                                                <span v-for="elgamalEncryption in ballot.ballot.a_bold">
                                                (<BigIntLabel :mpzValue="elgamalEncryption[0]"></BigIntLabel>,
                                                <BigIntLabel :mpzValue="elgamalEncryption[1]"></BigIntLabel>)
                                                </span>
                                            </v-flex>
                                        </v-layout>
                                        <v-layout row>
                                            <v-flex xy4 md4>Public voter credential:</v-flex>
                                            <v-flex x8 md8><BigIntLabel :mpzValue="ballot.ballot.x_hat"></BigIntLabel></v-flex>
                                        </v-layout>
                                        <v-layout row>
                                            <v-flex xy4 md4>Ballot-Proof:</v-flex>
                                            <v-flex xy8 md8>
                                                <span v-for="a in ballot.ballot.pi">
                                                <p v-for="i in a"><BigIntLabel :mpzValue="i"></BigIntLabel></p>
                                                </span>
                                            </v-flex>
                                        </v-layout>
                                    </v-card-text>
                                </v-card>
                            </v-expansion-panel-content>
                        </transition-group>

                    </DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Public Key" :isMpz=true :expandable=false confidentiality="public">
                        <BigIntLabel :mpzValue="electionAuthority.publicKey"></BigIntLabel>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Public Key Share" :isMpz=true :expandable=false confidentiality="public">
                        <BigIntLabel :mpzValue="electionAuthority.publicKeyShare"></BigIntLabel>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Secret Key Share" :isMpz=true :expandable=false confidentiality="secret">
                        <BigIntLabel :mpzValue="electionAuthority.secretKeyShare"></BigIntLabel>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4 v-if="expertMode">
                    <DataCard title="Points" :expandable=true confidentiality="secret">
                        Points of all voters
                        <ul id="list" slot="expandContent">
                            <li v-for="(voter, index) in electionAuthority.points">
                                Voter {{ index}}
                                <ul id="subList">
                                    <li v-for="point in voter">
                                        x:
                                        <BigIntLabel :mpzValue="point[0]"></BigIntLabel>
                                        y:
                                        <BigIntLabel :mpzValue="point[1]"></BigIntLabel>
                                    </li>
                                </ul>

                            </li>
                        </ul>
                    </DataCard>
                </v-flex>
            </v-layout>
        </div>
        <div v-else>
            <LoadingOverlay></LoadingOverlay>
        </div>
    </v-container>
</template>

<script>
    import { mapState, mapGetters } from 'vuex'
    import joinRoomMixin from '../../mixins/joinRoomMixin.js'

    export default {
      mixins: [joinRoomMixin],
      data: () => ({
        selectedAuthorityIndex: 0,
        show: false,
        ballotTransition: false,
        checkTransition: false,
        ballotTransitionClass: 'highlight',
        checkTransitionClass: 'bounce'
      }),
      mounted () {
        this.ballotTransition = false
        this.checkTransition = false
      },
      computed: {
        ...mapState({
          electionAuthorities: state => state.ElectionAuthority.electionAuthorities,
          expertMode: state => state.BulletinBoard.expertMode
        }),
        ...mapGetters({
          electionId: 'electionId'
        }),
        electionAuthority: {
          get: function () {
            return this.$store.getters.getElectionAuthority(this.selectedAuthorityIndex)
          }
        },
        checkBallotTasks: {
          get: function () {
            return this.$store.getters.getCheckBallotTasks(this.selectedAuthorityIndex)
          }
        },
        ballots: {
          get: function () {
            return this.$store.getters.getBallotsAndConfirmations(this.selectedAuthorityIndex)
          }
        },
        checkConfirmationTasks: {
          get: function () {
            return this.$store.getters.getCheckConfirmationTasks(this.selectedAuthorityIndex)
          }
        },
        confirmations: {
          get: function () {
            return this.$store.getters.getConfirmations(this.selectedAuthorityIndex)
          }
        },
        autoMode: {
          get: function () {
            return this.electionAuthority.autoCheck
          },
          set: function (value) {
            this.$store.dispatch('setAutoMode', {electionId: this.$route.params['id'], electionAuthorityId: this.selectedAuthorityIndex, newValue: value})
          }
        }
      },
      methods: {
        checkBallot: function (voterId) {
          this.$http.post('checkVote', {
            'election': this.$route.params['id'],
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
            'election': this.$route.params['id'],
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
            'election': this.$route.params['id'],
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
        checkConfirmation: function (voterId) {
          this.$http.post('checkConfirmation', {
            'election': this.$route.params['id'],
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
            'election': this.$route.params['id'],
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
            'election': this.$route.params['id'],
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
      },
      watch: {
        selectedAuthorityIndex: function (newAuthority) {
          // Transition animation is also shown when the selected authority has changed. As a workaround, temporarily remove the CSS transition class and re-assign it after some delay
          let self = this
          let savedTransitionClass = this.ballotTransitionClass
          let savedCheckTransitionClass = this.checkTransitionClass
          this.ballotTransitionClass = ''
          this.checkTransitionClass = ''
          setTimeout(function () {
            self.ballotTransitionClass = savedTransitionClass
            self.checkTransitionClass = savedCheckTransitionClass
          }, 2000)
        }
      }

    }
</script>

<style>
    .btn-toggle {
        width: 100%;
        background-color: transparent !important;
        margin-top: -5px !important;
    }

    .btn-toggle .btn {
        width: 33%;
        border-radius: 4px !important;

    }

    .btn-toggle--selected {
        box-shadow: none;
    }

    .highlight-enter-active {
        animation: highlight 2.0s;
    }

    @keyframes highlight {
        0% {
            background: inherit;
        }
        50% {
            background: rgba(11, 176, 255, 0.4);
        }
        100% {
            background: inherit;
        }
    }

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