<template>
    <transition-group tag="v-expansion-panel" name="highlight" class="expansion-panel--popout"
                      :appear="ballotTransition">
        <v-expansion-panel-content v-for="ballot in ballots" :key="ballot.id" ripple>
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
                            <v-chip left label outline color="red" v-if="ballot.validity === 4"
                                    v-t="'BallotList.credentialInvalid'"></v-chip>
                            <v-chip left label outline color="red" v-if="ballot.validity === 5"
                                    v-t="'BallotList.queryInvalid'"></v-chip>
                        </transition>
                    </v-flex>
                    <v-flex xs12 sm12 md3>

                        <span v-if="ballot.responses.length > 0 && authorityFilter === undefined">
                            Responses:
                            <transition-group name="highlight">
                                <TupleLabel v-for="(r, index) in ballot.responses" :tupleValue="r" title=""
                                            :icon="tupleLabelIcon(index+1)" :key="index"></TupleLabel>
                            </transition-group>
                        </span>
                        <span v-if="ballot.responses.length > 0 && authorityFilter !== undefined">
                            Response:
                            <transition name="highlight">
                                <TupleLabel :tupleValue="ballot.responses[authorityFilter]" title=""
                                            :icon="tupleLabelIcon(authorityFilter+1)"></TupleLabel>
                            </transition>
                        </span>
                    </v-flex>
                    <v-flex xs4 sm4 md2>
                        <transition name="highlight">
                            <v-chip left label outline color="green" v-if="hasValidConfirmation(ballot.confirmations)"
                                    v-t="'BallotList.confirmed'"></v-chip>
                            <v-chip left label outline color="red"
                                    v-else-if="hasInvalidConfirmations(ballot.confirmations)"
                                    v-t="'BallotList.hasInvalidConfirmations'"></v-chip>
                            <v-chip left label outline v-else v-t="'BallotList.unconfirmed'"></v-chip>
                        </transition>
                    </v-flex>
                    <v-flex xs8 sm8 md3>
                        <span v-if="getValidConfirmation(ballot.confirmations) !== null && authorityFilter === undefined">
                            Finalizations:
                            <transition-group name="highlight">
                                <TupleLabel
                                        v-for="(f,index) in getValidConfirmation(ballot.confirmations).finalizations"
                                        :tupleValue="f" title="" :icon="tupleLabelIcon(index+1)"
                                        :key="index"></TupleLabel>
                            </transition-group>
                        </span>
                        <span v-if="getValidConfirmation(ballot.confirmations) !== null && authorityFilter !== undefined">
                            Finalization:
                            <transition name="highlight">
                                <TupleLabel
                                        :tupleValue="getValidConfirmation(ballot.confirmations).finalizations[authorityFilter]"
                                        title="" :icon="tupleLabelIcon(authorityFilter+1)"></TupleLabel>
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
                            <span v-for="a in ballot.ballot.pi">
                            <p v-for="i in a"><BigIntLabel :mpzValue="i"></BigIntLabel></p>
                            </span>
                        </v-flex>
                    </v-layout>
                    <b>Confirmation history:</b>
                    <v-layout row v-for="(c,index) in ballot.confirmations" v-bind:key="c.confirmationId">
                        <v-flex xy1 md1></v-flex>
                        <v-flex xy2 md2 class="ballotTitle">Confirmation {{index+1}}</v-flex>
                        <v-flex xy2 md2>
                            <transition name="highlight">
                                <v-chip left label outline v-if="c.validity === 0"
                                        v-t="'BallotList.unchecked'"></v-chip>
                                <v-chip left label outline color="green" v-if="c.validity === 1"
                                        v-t="'BallotList.valid'"></v-chip>
                                <v-chip left label outline color="red" v-if="c.validity === 2"
                                        v-t="'BallotList.ballotProofInvalid'"></v-chip>
                                <v-chip left label outline color="red" v-if="c.validity === 4"
                                        v-t="'BallotList.credentialInvalid'"></v-chip>
                                <v-chip left label outline color="red" v-if="c.validity === 5"
                                        v-t="'BallotList.queryInvalid'"></v-chip>
                            </transition>
                        </v-flex>
                        <v-flex xy3 md3>
                            <span v-if="c.finalizations.length > 0 && authorityFilter === undefined">
                                Finalizations:
                                <transition-group name="highlight">
                                    <TupleLabel
                                                    v-for="(f,index) in c.finalizations"
                                                    :tupleValue="f" title="" :icon="tupleLabelIcon(index+1)"
                                                    :key="index"></TupleLabel>
                                </transition-group>
                            </span>
                            <span v-if="c.finalizations.length > 0 && authorityFilter !== undefined">
                                        Finalization:
                                <transition name="highlight">
                                    <TupleLabel
                                                    :tupleValue="c.finalizations[authorityFilter]"
                                                    title="" :icon="tupleLabelIcon(authorityFilter+1)"></TupleLabel>
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
        hasValidConfirmation: function (confirmations) {
          for (let confirmation of confirmations) {
            if (confirmation.validity === 1) {
              return true
            }
          }
          return false
        },
        getValidConfirmation: function (confirmations) {
          for (let confirmation of confirmations) {
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
        tupleLabelIcon: function (number) {
          return `mdi-numeric-${number}-box`
        }
      }

    }
</script>

<style>
    .ballotTitle {
        margin-top: 7px;
    }
</style>