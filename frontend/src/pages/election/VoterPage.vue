<template>
    <v-container grid-list-md>
        <div v-if="this.$store.state.loaded">
            <ContentTitle icon="mdi-account" :title="selectedVoterName || $t('Voter.title')">
                <v-btn flat color="blue" @click="changeVoter" class="changeVoterBtn">
                  <v-icon>mdi-account-multiple</v-icon>
                  {{ $t('Voter.select_voter') }}
                </v-btn>
            </ContentTitle>


            <!--<v-btn flat color="blue" v-if="this.$store.state.selectedVoter != null" @click="changeVoter()" class="changeVoterButton">Change Voter</v-btn>-->
            <div v-if="status < 1" v-t="'Voter.before_vote'"></div>
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
                            <v-card v-if="hasCheckBallotTask > -1">
                                <v-card-title primary-title>
                                    <div class="headline" v-t="'Voter.waiting_for_election_authority'"></div>
                                </v-card-title>
                                <v-card-text>
                                    {{ $t('Voter.authority_n_processing_vote', { n: hasCheckBallotTask + 1 }) }}
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
                                        <v-text-field :label="$t('voting_code')" v-model="votingCode" required></v-text-field>
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
                            <v-card v-if="hasCheckConfirmationTask > -1">
                                <v-card-title primary-title>
                                    <div class="headline" v-t="'Voter.waiting_for_election_authority'"></div>
                                </v-card-title>
                                <v-card-text>
                                    {{ $t('Voter.authority_n_processing_vote', { n: hasCheckConfirmationTask + 1 }) }}
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
                                        <v-text-field :label="$t('Voter.confirmation_code')" v-model="confirmationCode" required></v-text-field>
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
                                    <div class="headline" v-t="'Voter.vote_confirmation'"></div>
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
                            <ul>
                                <li>{{ $t('voting_code') }}: <b>{{ votingCard["votingCode"]}}</b></li>
                                <li>{{ $t('Voter.confirmation_code') }}: <b>{{ votingCard["confirmationCode"]}}</b></li>
                                <li>{{ $t('Voter.verification_codes') }}: <b>{{ votingCard["verificationCodes"]}}</b></li>
                                <li>{{ $t('Voter.finalization_code') }}: <b>{{ votingCard["finalizationCode"]}}</b></li>

                            </ul>
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

    export default {
      mixins: [joinRoomMixin],
      data: () => ({
        selection: [],
        votingCode: '',
        confirmationCode: ''

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
            if (this.selectedVoter != null) {
              return this.$store.getters.getVotingCard(this.selectedVoter)
            }
          }
        },
        selectedVoterName: {
          get () {
            if (this.$store.state.selectedVoter != null) {
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
        hasCheckBallotTask: {
          get: function () {
            return this.$store.getters.hasCheckBallotTask(this.$store.state.selectedVoter)
          }
        },
        hasCheckConfirmationTask: {
          get: function () {
            return this.$store.getters.hasCheckConfirmationTask(this.$store.state.selectedVoter)
          }
        }
      },
      methods: {
        changeVoter: function () {
          this.$store.commit('voterDialog', true)
        },
        castVote: function (manipulate) {
          let selection = this.selection.sort()
          if (manipulate) {
            selection[0] = (selection[0] + 1) % this.numberOfCandidates[0]
          }

          this.$http.post('castVote',
            {
              'election': this.$route.params['electionId'],
              'selection': this.selection.sort(),
              'voterId': this.selectedVoter,
              'votingCode': this.votingCode
            }
          ).then(response => {
            response.json().then((data) => {
              // success callback
              this.$toasted.success('Successfully cast vote')
            })
          }).catch(e => {
            this.$toasted.error(e.body.message)
          })
        },
        confirmVote: function () {
          this.$http.post('confirmVote',
            {
              'election': this.$route.params['electionId'],
              'voterId': this.selectedVoter,
              'confirmationCode': this.confirmationCode
            }
          ).then(response => {
            response.json().then((data) => {
              this.$toasted.success(this.$i18n.t('Voter.successfully_confirmed_vote'))
            })
          }).catch(e => {
            this.$toasted.error(e.body.message)
          })
        }
      },
      watch: {
        selectedVoter: function (newValue) {
          this.selection = []
          this.votingCode = ''
          this.confirmationCode = ''
        }
      }
    }
</script>
<style>
    .application--light .stepper {
        background: transparent !important;
    }

    .stepper {
        box-shadow: none !important;
        margin-top: -20px;
    }
    .application--light .stepper .stepper__step__step{
        box-shadow: 0 0 2px 2px rgba(0,0,0,.2), 0px 0px 0px 0px rgba(0,0,0,.14), 0 1px 10px rgba(0,0,0,.12);

    }

    .stepper__step--active .stepper__step__step, .stepper__step--complete .stepper__step__step {
        background: #696969 ;
    }
    .application--light .stepper .stepper__step:not(.stepper__step--active):not(.stepper__step--complete):not(.stepper__step--error) .stepper__step__step {
        background: rgba(0, 0, 0, 0.2) !important;
    }

    .electionForm{
        width:100%;
        margin-bottom: 20px;
    }

    .changeVoterBtn{
        position: absolute !important;right: 35px;margin-top: 25px;
    }
</style>
