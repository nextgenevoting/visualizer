<template>
    <div>
        <ResponsesTupleDialog
                :tuple="selectedResponse" v-if="selectedResponse !== null" :visible="responseDialogVisible" :popupTitle="responseTitleString(responseIndex)" @close="responseDialogVisible = false"
        />
        <FinalizationsTupleDialog
                :tuple="selectedFinalization" v-if="selectedFinalization !== null" :visible="finalizationDialogVisible" :popupTitle="finalizationTitleString(finalizationIndex)" @close="finalizationDialogVisible = false"
        />
        <transition-group tag="v-expansion-panel" name="highlight" class="expansion-panel--popout" :appear="ballotTransition">
            <p v-if="ballots.length === 0" v-bind:key="0" v-t="'BallotList.noBallots'"></p>
            <v-expansion-panel-content v-for="ballot in ballots" :key="ballot.id">
                <div slot="header">
                    <v-layout row wrap>
                        <v-flex xs12 sm2 md2 class="ballotTitle">
                            {{ $t('ElectionAuthority.ballot_of_voter_n', { n: ballot.voterId + 1 }) }}
                        </v-flex>
                        <v-flex xs6 sm2 md2>
                            <transition name="highlight">
                                <v-chip left label outline v-if="ballot.validity === 0" v-t="'BallotList.unchecked'"></v-chip>
                                <v-chip left label outline color="green" v-if="ballot.validity === 1" v-t="'BallotList.validBallot'"></v-chip>
                                <v-chip left label outline color="red" v-if="ballot.validity === 2" v-t="'BallotList.ballotProofInvalid'"></v-chip>
                                <v-chip left label outline color="red" v-if="ballot.validity === 3" v-t="'BallotList.alreadyHasBallot'"></v-chip>
                                <v-chip left label outline color="red" v-if="ballot.validity === 4" v-t="'BallotList.credentialInvalid'"></v-chip>
                                <v-chip left label outline color="red" v-if="ballot.validity === 5" v-t="'BallotList.queryInvalid'"></v-chip>
                            </transition>
                        </v-flex>
                        <v-flex xs6 sm3 md3 style="padding-top: 9px;">
                            <span v-if="hasResponses(ballot) && authorityFilter === undefined">
                                {{$t('responses')}}:
                                <transition-group name="highlight">
                                    <v-btn small icon v-for="(r, index) in ballot.responses" v-if="r !== null" @click.stop="showResponse(r,index+1)" :key="index"><v-icon>{{tupleLabelIconString(index+1)}}</v-icon></v-btn>
                                </transition-group>
                            </span>
                            <span v-if="hasResponses(ballot) && authorityFilter !== undefined">
                                {{$t('response')}}:
                                <transition name="highlight">
                                    <v-btn small icon @click.stop="showResponse(ballot.responses[authorityFilter], authorityFilter+1)" v-if="ballot.responses[authorityFilter] !== null"><v-icon>{{tupleLabelIconString(authorityFilter+1)}}</v-icon></v-btn>
                                </transition>
                            </span>
                        </v-flex>
                        <v-flex xs6 sm2 md2>
                            <transition name="highlight">
                                <v-chip left label outline color="green" v-if="hasValidConfirmation(ballot)" v-t="'BallotList.confirmed'"></v-chip>
                                <v-chip left label outline color="red" v-else-if="hasInvalidConfirmations(ballot.confirmations)" v-t="'BallotList.hasInvalidConfirmations'"></v-chip>
                                <v-chip left label outline v-else v-t="'BallotList.unconfirmed'"></v-chip>
                            </transition>
                        </v-flex>
                        <v-flex xs6 sm3 md3 style="padding-top: 9px;">
                            <span v-if="getValidConfirmation(ballot) !== null && authorityFilter === undefined">
                                {{$t('finalizations')}}:
                                <transition-group name="highlight">
                                    <v-btn small icon v-for="(f, index) in getValidConfirmation(ballot).finalizations" v-if="f !== null" @click.stop="showFinalization(f,index+1)" :key="index"><v-icon>{{tupleLabelIconString(index+1)}}</v-icon></v-btn>
                                </transition-group>
                            </span>
                            <span v-if="getValidConfirmation(ballot) !== null && authorityFilter !== undefined">
                                {{$t('finalization')}}:
                               <transition name="highlight">
                                    <v-btn small icon @click.stop="showFinalization(getValidConfirmation(ballot).finalizations[authorityFilter], authorityFilter+1)" v-if="getValidConfirmation(ballot).finalizations[authorityFilter] !== null"><v-icon>{{tupleLabelIconString(authorityFilter+1)}}</v-icon></v-btn>
                                </transition>
                            </span>
                        </v-flex>
                    </v-layout>
                </div>
                <v-card>
                    <v-card-text class="grey lighten-3">
                        <v-layout row wrap>
                            <v-flex xs2 md2 v-t="'ElectionAuthority.encrypted_selections'"></v-flex>
                            <v-flex xs10 md10>
                                <span v-for="(elgamalEncryption, i) in ballot.ballot.a_bold">
                                  (<BigIntLabel :mpzValue="elgamalEncryption[0]"></BigIntLabel>,
                                  <BigIntLabel :mpzValue="elgamalEncryption[1]"></BigIntLabel>)<span v-if="i < ballot.ballot.a_bold.length - 1">, </span>
                                </span>
                            </v-flex>
                        </v-layout>
                        <v-layout row wrap>
                            <v-flex xs2 md2 v-t="'ElectionAuthority.public_voter_credential'"></v-flex>
                            <v-flex xs10 md10>
                                <BigIntLabel :mpzValue="ballot.ballot.x_hat"></BigIntLabel>
                            </v-flex>
                        </v-layout>
                        <v-layout row wrap>
                            <v-flex xs2 md2 v-t="'ElectionAuthority.ballot_proof'"></v-flex>
                            <v-flex xs10 md10>
                                (<BigIntLabel :mpzValue="ballot.ballot.pi[0][0]"></BigIntLabel>,
                                <BigIntLabel :mpzValue="ballot.ballot.pi[0][1]"></BigIntLabel>,
                                <BigIntLabel :mpzValue="ballot.ballot.pi[0][2]"></BigIntLabel>),
                                (<BigIntLabel :mpzValue="ballot.ballot.pi[1][0]"></BigIntLabel>,
                                <BigIntLabel :mpzValue="ballot.ballot.pi[1][1]"></BigIntLabel>,
                                <BigIntLabel :mpzValue="ballot.ballot.pi[1][2]"></BigIntLabel>)
                            </v-flex>
                        </v-layout>
                        <v-layout row wrap>
                            <v-flex xs2 md2 v-t="'timestamp'"></v-flex>
                            <v-flex xs10 md10>
                                {{ ballot.timestamp }}
                            </v-flex>
                        </v-layout>
                        <b>{{$t('confirmation_history')}}</b>
                        <v-layout row wrap v-for="(c,index) in ballot.confirmations" v-bind:key="c.confirmationId">
                            <v-flex xs1 md1></v-flex>
                            <v-flex xs2 md2 class="ballotTitle">{{$t('confirmation')}} {{ index + 1 }}</v-flex>
                            <v-flex xs4 md4 style="padding-top: 9px;">
                                {{ c.timestamp }}
                            </v-flex>
                            <v-flex xs2 md2>
                                <transition name="highlight">
                                    <v-chip left label outline v-if="c.validity === 0" v-t="'BallotList.unchecked'"></v-chip>
                                    <v-chip left label outline color="green" v-if="c.validity === 1" v-t="'BallotList.valid'"></v-chip>
                                    <v-chip left label outline color="red" v-if="c.validity === 2" v-t="'BallotList.ballotProofInvalid'"></v-chip>
                                    <v-chip left label outline color="red" v-if="c.validity === 3" v-t="'BallotList.confirmationHasNoBallot'"></v-chip>
                                    <v-chip left label outline color="red" v-if="c.validity === 4" v-t="'BallotList.alreadyHasConfirmation'"></v-chip>
                                    <v-chip left label outline color="red" v-if="c.validity === 5" v-t="'BallotList.credentialInvalid'"></v-chip>
                                </transition>
                            </v-flex>
                            <v-flex xs3 md3 style="padding-top: 9px;">
                                <span v-if="getValidConfirmation(ballot) !== null && authorityFilter === undefined">
                                {{$t('finalizations')}}:
                                <transition-group name="highlight">
                                    <v-btn small icon v-for="(f, index) in getValidConfirmation(ballot).finalizations" v-if="f !== null" @click.stop="showFinalization(f,index+1)" :key="index"><v-icon class="tupleButton">{{tupleLabelIconString(index+1)}}</v-icon></v-btn>
                                </transition-group>
                            </span>
                                <span v-if="getValidConfirmation(ballot) !== null && authorityFilter !== undefined">
                                {{$t('finalization')}}:
                               <transition name="highlight">
                                    <v-btn small icon @click.stop="showFinalization(getValidConfirmation(ballot).finalizations[authorityFilter], authorityFilter+1)" v-if="getValidConfirmation(ballot).finalizations[authorityFilter] !== null"><v-icon class="tupleButton">{{tupleLabelIconString(authorityFilter+1)}}</v-icon></v-btn>
                                </transition>
                            </span>
                            </v-flex>
                        </v-layout>
                    </v-card-text>
                </v-card>
            </v-expansion-panel-content>
        </transition-group>
    </div>
</template>

<script>
export default {
  data: () => ({
    ballotTransition: false,
    selectedResponse: null,
    responseDialogVisible: false,
    responseIndex: 0,
    selectedFinalization: null,
    finalizationDialogVisible: false,
    finalizationIndex: 0
  }),
  props: {
    ballots: {
      type: Array,
      required: true
    },
    authorityFilter: {
      type: Number,
      requried: false
    }
  },
  mounted () {
    this.ballotTransition = false
  },
  methods: {
    showResponse: function (response, responseIndex) {
      this.responseDialogVisible = true
      this.selectedResponse = response
      this.responseIndex = responseIndex
    },
    showFinalization: function (finalization, finalizationIndex) {
      this.finalizationDialogVisible = true
      this.selectedFinalization = finalization
      this.finalizationIndex = finalizationIndex
    },
    hasResponses: function (ballot) {
      return ballot.responses.length > 0 && ballot.responses.reduce((acc, val) => (val !== null) ? acc.concat(val) : acc, []).length > 0
    },
    hasValidConfirmation: function (ballot) {
      for (let confirmation of ballot.confirmations) {
        if (confirmation.validity === 1) {
          return true
        }
      }
      return false
    },
    getValidConfirmation: function (ballot) {
      for (let confirmation of ballot.confirmations) {
        if (confirmation.validity === 1) {
          return confirmation
        }
      }
      return null
    },
    hasInvalidConfirmations: function (confirmations) {
      for (let confirmation of confirmations) {
        if (confirmation.validity > 1) {
          return true
        }
      }
      return false
    },
    tupleLabelIconString: function (number) {
      return `mdi-numeric-${number}-box`
    },
    responseTitleString: function (number) {
      return this.$i18n.t('oblivious_transfer_response_n', { n: number })
    },
    finalizationTitleString: function (number) {
      return this.$i18n.t('finalization_n', { n: number })
    }
  }
}
</script>

<style>
.ballotTitle {
    margin-top: 7px;
}

.btn{
    margin: 0;
}

.expansion-panel--popout .expansion-panel__container, .expansion-panel--inset .expansion-panel__container {
    max-width: 100% !important;
}
.tupleButton{
    color: rgba(0,0,0,.54) !important;
}
</style>
