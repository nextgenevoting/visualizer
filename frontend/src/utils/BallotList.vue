<template>
    <transition-group tag="v-expansion-panel" name="highlight" class="expansion-panel--popout" :appear="ballotTransition">
        <v-expansion-panel-content v-for="ballot in ballots" :key="ballot.id">
            <div slot="header">
                <v-layout row>
                    <v-flex xs2 sm2 md1 class="ballotTitle">
                        {{ $t('ElectionAuthority.ballot_of_voter_n', {n: ballot.voterId + 1}) }}
                    </v-flex>
                    <v-flex xs4 sm4 md2>
                        <transition name="highlight">
                            <v-chip left label outline v-if="ballot.validity === 0"
                                    v-t="'BallotList.unchecked'"></v-chip>
                            <v-chip left label outline color="green" v-if="ballot.validity === 1"
                                    v-t="'BallotList.validBallot'"></v-chip>
                            <v-chip left label outline color="red" v-if="ballot.validity === 2"
                                    v-t="'BallotList.ballotProofInvalid'"></v-chip>
                            <v-chip left label outline color="red" v-if="ballot.validity === 3"
                                    v-t="'BallotList.alreadyHasBallot'"></v-chip>
                            <v-chip left label outline color="red" v-if="ballot.validity === 4"
                                    v-t="'BallotList.credentialInvalid'"></v-chip>
                            <v-chip left label outline color="red" v-if="ballot.validity === 5"
                                    v-t="'BallotList.queryInvalid'"></v-chip>
                        </transition>
                    </v-flex>
                    <v-flex xs12 sm12 md3 style="padding-top: 9px;">
                        <span v-if="hasResponses(ballot) && authorityFilter === undefined">
                            Responses:
                            <transition-group name="highlight">
                                <TupleLabel v-for="(r, index) in ballot.responses" v-if="r !== null" :tupleValue="r" :popupTitle="responseTitleString(index+1)" title=""
                                            :icon="tupleLabelIconString(index+1)" :key="index"></TupleLabel>
                            </transition-group>
                        </span>
                        <span v-if="hasResponses(ballot) && authorityFilter !== undefined">
                            Response:
                            <transition name="highlight">
                                <TupleLabel  v-if="ballot.responses[authorityFilter] !== null" :tupleValue="ballot.responses[authorityFilter]" :popupTitle="responseTitleString(authorityFilter+1)" title=""
                                            :icon="tupleLabelIconString(authorityFilter+1)"></TupleLabel>
                            </transition>
                        </span>
                    </v-flex>
                    <v-flex xs4 sm4 md3>
                        <transition name="highlight">
                            <v-chip left label outline color="green" v-if="hasValidConfirmation(ballot)"
                                    v-t="'BallotList.confirmed'"></v-chip>
                            <v-chip left label outline color="red"
                                    v-else-if="hasInvalidConfirmations(ballot.confirmations)"
                                    v-t="'BallotList.hasInvalidConfirmations'"></v-chip>
                            <v-chip left label outline v-else v-t="'BallotList.unconfirmed'"></v-chip>
                        </transition>
                    </v-flex>
                    <v-flex xs8 sm8 md3 style="padding-top: 9px;">
                        <span v-if="getValidConfirmation(ballot) !== null && authorityFilter === undefined">
                            Finalizations:
                            <transition-group name="highlight">
                                <TupleLabel
                                        v-for="(f,index) in getValidConfirmation(ballot).finalizations" v-if="f !== null"
                                        :tupleValue="f" title="" :icon="tupleLabelIconString(index+1)"
                                        :key="index" :popupTitle="finalizationTitleString(index+1)"></TupleLabel>
                            </transition-group>
                        </span>
                        <span v-if="getValidConfirmation(ballot) !== null && authorityFilter !== undefined">
                            Finalization:
                            <transition name="highlight">
                                <TupleLabel
                                        :tupleValue="getValidConfirmation(ballot).finalizations[authorityFilter]" v-if="getValidConfirmation(ballot).finalizations[authorityFilter] !== null"
                                        title="" :icon="tupleLabelIconString(authorityFilter+1)" :popupTitle="finalizationTitleString(authorityFilter+1)"></TupleLabel>
                            </transition>
                        </span>
                    </v-flex>
                </v-layout>
            </div>
            <v-card>
                <v-card-text class="grey lighten-3">
                    <v-layout row>
                        <v-flex xy2 md2 v-t="'ElectionAuthority.encrypted_selections'"></v-flex>
                        <v-flex x10 md10>
                            <span v-for="elgamalEncryption in ballot.ballot.a_bold">
                                (<BigIntLabel :mpzValue="elgamalEncryption[0]"></BigIntLabel>,
                                  <BigIntLabel :mpzValue="elgamalEncryption[1]"></BigIntLabel>)
                            </span>
                        </v-flex>
                    </v-layout>
                    <v-layout row>
                        <v-flex xy2 md2 v-t="'ElectionAuthority.public_voter_credential'"></v-flex>
                        <v-flex xy10 md10>
                            <BigIntLabel :mpzValue="ballot.ballot.x_hat"></BigIntLabel>
                        </v-flex>
                    </v-layout>
                    <v-layout row>
                        <v-flex xy2 md2 v-t="'ElectionAuthority.ballot_proof'"></v-flex>
                        <v-flex x10 md10>
                            <!--<span v-for="a in ballot.ballot.pi">
                            <p v-for="i in a"><BigIntLabel :mpzValue="i"></BigIntLabel></p>
                            </span>-->
                            (<BigIntLabel :mpzValue="ballot.ballot.pi[0][0]"></BigIntLabel>, <BigIntLabel :mpzValue="ballot.ballot.pi[0][1]"></BigIntLabel>, <BigIntLabel :mpzValue="ballot.ballot.pi[0][2]"></BigIntLabel>),
                            (<BigIntLabel :mpzValue="ballot.ballot.pi[1][0]"></BigIntLabel>, <BigIntLabel :mpzValue="ballot.ballot.pi[1][1]"></BigIntLabel>, <BigIntLabel :mpzValue="ballot.ballot.pi[1][2]"></BigIntLabel>)
                        </v-flex>
                    </v-layout>
                    <v-layout row>
                        <v-flex xy2 md2 v-t="'timestamp'"></v-flex>
                        <v-flex x10 md10>
                            {{ ballot.timestamp }}
                        </v-flex>
                    </v-layout>
                    <b>Confirmation history:</b>
                    <v-layout row v-for="(c,index) in ballot.confirmations" v-bind:key="c.confirmationId">
                        <v-flex xy1 md1></v-flex>
                        <v-flex xy2 md2 class="ballotTitle">Confirmation {{index+1}}</v-flex>
                        <v-flex xy4 md4 style="padding-top: 9px;">
                            {{ c.timestamp }}
                        </v-flex>
                        <v-flex xy2 md2>
                            <transition name="highlight">
                                <v-chip left label outline v-if="c.validity === 0"
                                        v-t="'BallotList.unchecked'"></v-chip>
                                <v-chip left label outline color="green" v-if="c.validity === 1"
                                        v-t="'BallotList.valid'"></v-chip>
                                <v-chip left label outline color="red" v-if="c.validity === 2"
                                        v-t="'BallotList.ballotProofInvalid'"></v-chip>
                                <v-chip left label outline color="red" v-if="c.validity === 3"
                                        v-t="'BallotList.confirmationHasNoBallot'"></v-chip>
                                <v-chip left label outline color="red" v-if="c.validity === 4"
                                        v-t="'BallotList.alreadyHasConfirmation'"></v-chip>
                                <v-chip left label outline color="red" v-if="c.validity === 5"
                                        v-t="'BallotList.credentialInvalid'"></v-chip>
                            </transition>
                        </v-flex>
                        <v-flex xy3 md3 style="padding-top: 9px;">
                            <span v-if="c.finalizations.length > 0 && authorityFilter === undefined">
                                Finalizations:
                                <transition-group name="highlight">
                                    <TupleLabel
                                                    v-for="(f,index) in c.finalizations" v-if="f !== null"
                                                    :tupleValue="f" title="" :icon="tupleLabelIconString(index+1)"
                                                    :key="index"></TupleLabel>
                                </transition-group>
                            </span>
                            <span v-if="c.finalizations.length > 0 && authorityFilter !== undefined">
                                        Finalization:
                                <transition name="highlight">
                                    <TupleLabel
                                                    :tupleValue="c.finalizations[authorityFilter]" v-if="c.finalizations[authorityFilter] !== null"
                                                    title="" :icon="tupleLabelIconString(authorityFilter+1)"></TupleLabel>
                                </transition>
                            </span>
                        </v-flex>
                    </v-layout>
                </v-card-text>
            </v-card>
        </v-expansion-panel-content>
    </transition-group>
</template>

<script>
    export default {
      data: () => ({
        ballotTransition: false
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
        hasResponses: function (ballot) {
          return ballot.responses.length > 0
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
          return `Response of authority ${number}`
        },
        finalizationTitleString: function (number) {
          return `Finalization of authority ${number}`
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
</style>