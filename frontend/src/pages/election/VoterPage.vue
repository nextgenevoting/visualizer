<template>
    <v-container grid-list-md>
        <div v-if="this.$store.state.loaded">
            <ContentTitle icon="mdi-account" :title="selectedVoterName || $t('Voter.title')">
                <v-btn flat color="blue" @click="changeVoter" class="changeVoterBtn">
                  <v-icon left>mdi-account-multiple</v-icon>
                  {{ $t('Voter.select_voter') }}
                </v-btn>
            </ContentTitle>

            <div v-if="status < 1" v-t="'Voter.before_vote'"></div><!-- TODO when a voter is first selected, this text is still shown (bug?) -->
            <div v-else-if="status >= 4" v-t="'Voter.voting_closed'"></div>
            <div v-else>
                <v-flex xy12 md6 v-if="selectedVoter == null" v-t="'Voter.choose_voter_first'"></v-flex>
                <v-flex xy12 md12 v-else>
                    <v-stepper color="blue" alt-labels :value="voter.status + 1">
                        <v-stepper-header>
                            <v-stepper-step step="1" :complete="voter.status >= 1">{{$t('vote_casting')}}</v-stepper-step>
                            <v-divider></v-divider>
                            <v-stepper-step step="2" :complete="voter.status >= 2">{{$t('confirmation')}}</v-stepper-step>
                            <v-divider></v-divider>
                            <v-stepper-step step="3" :complete="voter.status >= 3">{{$t('finalization')}}</v-stepper-step>
                        </v-stepper-header>
                    </v-stepper>
                    <div class="layout row wrap">
                        <!-- 1. Vote Cast -->
                        <v-flex v-if="voter.status == 0" x12 md6>
                            <v-card v-if="ballotCheckAuthorityIndex > -1">
                                <v-card-title primary-title>
                                    <div class="headline" v-t="'Voter.waiting_for_election_authority'"></div>
                                </v-card-title>
                                <v-card-text>
                                    {{ $t('Voter.authority_n_processing_vote', { n: ballotCheckAuthorityIndex + 1 }) }}
                                    <v-progress-linear v-bind:indeterminate="true"></v-progress-linear>
                                </v-card-text>
                            </v-card>
                            <v-card v-else>
                                <v-card-title primary-title>
                                    <div class="headline" v-t="'vote_casting'"></div>
                                </v-card-title>
                                <v-card-text>
                                    <v-form ref="form" class="votingForm" lazy-validation>

                                    <ul v-for="(i, index) in numberOfParallelElections" class="electionForm">
                                        {{ $t('Voter.your_selection_for_election_n', { n: index + 1 }) }}
                                        <li v-for="candidate in candidatesForElection[index]">
                                            <v-checkbox :label="candidate.name" v-model="selection" :value="candidate.index" color="blue" hide-details></v-checkbox>
                                        </li>
                                    </ul>
                                        <v-text-field :label="$t('voting_code')" v-model="codes.voting" required></v-text-field>
                                    </v-form>

                                </v-card-text>
                                <v-card-actions>
                                    <v-btn flat color="blue" @click="castVote(false)">{{ $t('cast_vote') }}</v-btn>
                                    <v-btn flat @click="castVote(true)">
                                      <img src="/public/spy.png" />
                                      {{ $t('Voter.manipulate_selection') }}
                                    </v-btn>
                                </v-card-actions>
                            </v-card>

                        </v-flex>
                        <!-- 2. Vote Confirmation -->
                        <v-flex v-if="voter.status == 1" x12 md6>
                            <v-card v-if="confirmationCheckAuthorityIndex > -1">
                                <v-card-title primary-title>
                                    <div class="headline" v-t="'Voter.waiting_for_election_authority'"></div>
                                </v-card-title>
                                <v-card-text>
                                    {{ $t('Voter.authority_n_processing_vote', { n: confirmationCheckAuthorityIndex + 1 }) }}
                                    <v-progress-linear v-bind:indeterminate="true"></v-progress-linear>
                                </v-card-text>
                            </v-card>
                            <v-card v-else>
                                <v-card-title primary-title>
                                    <div class="headline" v-t="'Voter.vote_confirmation'"></div>
                                </v-card-title>
                                <v-card-text>
                                    <v-form ref="form" class="confirmationForm" lazy-validation>
                                        <p v-t="'Voter.check_displayed_codes'"></p><br><br>
                                        <div>
                                        <ul>
                                            <li v-for="(verificationCode, index) in voter.verificationCodes">
                                                {{ $t('Voter.verification_code_n', { n: index + 1 }) }}
                                                <b>{{ verificationCode }}</b>
                                            </li>
                                        </ul><br>
                                        </div>
                                        <p v-t="'Voter.confirm_vote_with_code'"></p>
                                        <v-text-field :label="$t('Voter.confirmation_code')" v-model="codes.confirmation" required></v-text-field>
                                    </v-form>

                                </v-card-text>
                                <v-card-actions>
                                    <v-btn flat color="blue" @click="confirmVote()">
                                      {{ $t('Voter.confirm_vote') }}
                                    </v-btn>
                                    <v-btn flat>
                                      {{ $t('cancel') }}
                                    </v-btn>
                                </v-card-actions>
                            </v-card>

                        </v-flex>
                        <!-- 3. Vote Finalization -->
                        <v-flex v-if="voter.status == 2" x12 md6>
                            <v-card>
                                <v-card-title primary-title>
                                    <div class="headline" v-t="'Voter.vote_finalization'"></div>
                                </v-card-title>
                                <v-card-text>
                                    {{ $t('Voter.you_have_confirmed_your_vote') }}:<br><br>
                                    <v-form ref="form" class="finalizationForm">
                                        {{ $t('Voter.finalization_code') }}: <b>{{ voter.finalizationCode }}</b>
                                    </v-form>
                                </v-card-text>
                            </v-card>
                        </v-flex>
                        <v-flex x12 md6>
                            <VotingCard :card="votingCard" :state="voter.status" :candidates="candidatesForElection" :codes="codes"></VotingCard>
                        </v-flex>
                    </div>
                </v-flex>
            </div>
        </div>
        <div v-else>
            <LoadingOverlay></LoadingOverlay>
        </div>
        <SelectVoterDialog></SelectVoterDialog>
    </v-container>
</template>

<script>
    import { mapState, mapGetters } from 'vuex'
    import joinRoomMixin from '../../mixins/joinRoomMixin.js'
    import * as _ from 'lodash'

    export default {
      mixins: [joinRoomMixin],
      data: () => ({
        selection: [],
        codes: {
          voting: '',
          confirmation: ''
        }
      }),
      computed: {
        ...mapState({
          selectedVoter: state => state.selectedVoter,
          numberOfParallelElections: state => state.BulletinBoard.numberOfParallelElections,
          candidates: state => state.BulletinBoard.candidates,
          numberOfCandidates: state => state.BulletinBoard.numberOfCandidates,
          publicKey: state => state.BulletinBoard.publicKey
        }),
        ...mapGetters({
          electionId: 'electionId',
          status: 'status'
        }),
        voter: {
          get: function () {
            return this.$store.getters.getVoter(this.selectedVoter)
          }
        },
        votingCard: {
          get: function () {
            if (this.selectedVoter !== null) {
              return this.$store.getters.getVotingCard(this.selectedVoter)
            }
          }
        },
        selectedVoterName: {
          get: function () {
            if (this.$store.state.selectedVoter !== null) {
              return this.$store.getters.getVoter(this.$store.state.selectedVoter).name
            } else {
              return ''
            }
          }
        },
        candidatesForElection: {
          get: function () {
            var candidatesForElections = []
            for (var j = 0; j < this.numberOfParallelElections; j++) {
              var startIndex = 0
              var candidates = []

              for (var i = 0; i < j; i++) {
                startIndex += this.numberOfCandidates[i]
              }
              for (i = 0; i < this.numberOfCandidates[j]; i++) {
                candidates.push({
                  name: this.candidates[startIndex + i],
                  index: startIndex + i,
                  checked: false
                })
              }
              candidatesForElections.push(candidates)
            }
            return candidatesForElections
          }
        },
        ballotCheckAuthorityIndex: {
          get: function () {
            return this.$store.getters.ballotCheckAuthorityIndex(this.$store.state.selectedVoter)
          }
        },
        confirmationCheckAuthorityIndex: {
          get: function () {
            return this.$store.getters.confirmationCheckAuthorityIndex(this.$store.state.selectedVoter)
          }
        }
      },
      methods: {
        changeVoter: function () {
          this.$store.commit('voterDialog', true)
        },
        castVote: _.debounce(function (manipulate) {
          let selection = this.selection.sort()
          if (manipulate) {
            selection[0] = (selection[0] + 1) % this.numberOfCandidates[0]
          }
          this.$http.post('castVote',
            {
              'election': this.$route.params['electionId'],
              'selection': this.selection.sort(),
              'voterId': this.selectedVoter,
              'votingCode': this.codes.voting
            }
          ).then(response => {
            response.json().then((data) => {
            })
          }).catch(e => {
            this.$toasted.error(e.body.message)
          })
        }, 200),
        confirmVote: _.debounce(function () {
          this.$http.post('confirmVote',
            {
              'election': this.$route.params['electionId'],
              'voterId': this.selectedVoter,
              'ballotId': this.voter.validBallot,
              'confirmationCode': this.codes.confirmation
            }
          ).then(response => {
            response.json().then((data) => {
            })
          }).catch(e => {
            this.$toasted.error(e.body.message)
          })
        }, 200)
      },
      watch: {
        selectedVoter: function (newValue) {
          this.selection = []
          this.codes.voting = ''
          this.codes.confirmation = ''
        }
      }
    }
</script>
<style>

    .electionForm{
        width:100%;
        margin-bottom: 20px;
    }

    .changeVoterBtn{
        position: absolute !important;right: 35px;margin-top: 25px;
    }
</style>
