<template>
    <v-container grid-list-md :fluid="fluidLayout">
        <div v-if="this.$store.state.loaded">
            <ContentTitle customicon="customicon icon-bulletin-board" :title="$t('BulletinBoard.title')"></ContentTitle>

            <h5 v-t="'BulletinBoard.pre_election_data'"></h5>
            <v-layout row wrap>
                <v-flex xs12 sm4 md4>
                    <DataCard :title="$t('BulletinBoard.unique_election_identifier')" :tooltip="$t('BulletinBoard.unique_election_identifier_tooltip')" :expandable=false confidentiality="public">
                        <ByteArrayLabel :value="electionId" :title="$t('BulletinBoard.unique_election_identifier')"></ByteArrayLabel></DataCard>
                </v-flex>

                <!--<v-flex xs12 sm4 md4>
                    <DataCard :title="$t('status')" :tooltip="$t('status_tooltip')" :expandable=false confidentiality="public">{{ statusText }}</DataCard>
                </v-flex>-->

                <v-flex xs12 sm4 md4>
                    <DataCard :title="$t('BulletinBoard.parallel_elections')" :tooltip="$t('BulletinBoard.parallel_elections_tooltip')" :expandable=false confidentiality="public">{{ numberOfParallelElections }}</DataCard>
                </v-flex>

                <v-flex xs12 sm4 md4>
                    <DataCard :title="$t('number_of_candidates')" :tooltip="$t('number_of_candidates_tooltip')" :expandable=false confidentiality="public">
                        <template v-for="(candidates, index) in numberOfCandidates">
                            {{candidates}}<span v-if="index < numberOfCandidates.length-1">, </span>
                        </template>
                    </DataCard>
                </v-flex>


                <v-flex xs12 sm8 md8>
                    <DataCard :title="$t('candidates')" :tooltip="$t('candidates_tooltip')" :expandable=false confidentiality="public">
                        <template v-for="(candidate, index) in candidates">
                            {{candidate}}<span v-if="index < candidates.length-1">, </span>
                        </template>
                    </DataCard>
                </v-flex>


                <v-flex xs12 sm4 md4>
                    <DataCard :title="$t('voters')" :tooltip="$t('voters_tooltip')" :expandable=false confidentiality="public">
                        <template v-for="(v, index) in voters">
                            {{v}}<span v-if="index < voters.length-1">, </span>
                        </template>
                    </DataCard>
                </v-flex>


                <v-flex xs12 sm4 md4>
                    <DataCard :title="$t('public_key')" :tooltip="$t('public_key_tooltip')" :isMpz=true :expandable=false confidentiality="public">
                        <BigIntLabel :mpzValue="publicKey"></BigIntLabel>
                    </DataCard>
                </v-flex>

                <v-flex xs12 sm4 md4>
                    <DataCard :title="$t('number_of_selections')" :tooltip="$t('number_of_selections_tooltip')" :expandable=false confidentiality="public">
                        <template v-for="(k, index) in numberOfSelections">
                            {{k}}<span v-if="index < numberOfSelections.length-1">, </span>
                        </template>
                    </DataCard>
                </v-flex>

                <v-flex xs12 sm4 md4>
                    <DataCard :title="$t('counting_circles')" :tooltip="$t('counting_circles_tooltip')" :expandable=false confidentiality="public">
                        <template v-for="(c, index) in countingCircles">
                            {{c}}<span v-if="index < countingCircles.length-1">, </span>
                        </template>
                    </DataCard>
                </v-flex>
            </v-layout>

            <h5 v-if="status >= 3" v-t="'BulletinBoard.election_data'"></h5>
            <v-layout row wrap>
                <v-flex xs12 sm12 md12>
                    <DataCard :title="$t('ballots')" :tooltip="$t('BulletinBoard.ballots_tooltip')" :expandable=false confidentiality="encrypted">
                        <BallotList :ballots="ballots"></BallotList>
                    </DataCard>
                </v-flex>
            </v-layout>

            <h5 v-if="status >= 4" v-t="'post_election_data'"></h5>
            <v-layout row wrap v-if="status >= 4">
                <v-flex xs12 md12>
                    <DataCard  :title="$t('shuffle_proofs')" :tooltip="$t('shuffle_proofs_tooltip')" :expandable=false confidentiality="public">
                        <v-expansion-panel class="expansion-panel--popout">
                            <v-expansion-panel-content v-for="(shuffleProof, index) in shuffleProofs" :key="index">
                                <div slot="header">{{ $t('BulletinBoard.shuffle_proofs_of_election_authority', { a: index + 1 }) }}</div>
                                <v-card>
                                    <v-card-text class="grey lighten-3">
                                        <v-layout row wrap>
                                            <v-flex xs2 md2>t:</v-flex>
                                            <v-flex xs10 md10>
                                              (<BigIntLabel :mpzValue="shuffleProof[0][0]"></BigIntLabel>,
                                              <BigIntLabel :mpzValue="shuffleProof[0][1]"></BigIntLabel>,
                                              <BigIntLabel :mpzValue="shuffleProof[0][2]"></BigIntLabel>,
                                              <TupleLabel :tupleValue="shuffleProof[0][3]"></TupleLabel>,
                                              <TupleLabel :tupleValue="shuffleProof[0][4]"></TupleLabel>)
                                            </v-flex>
                                        </v-layout>
                                        <v-layout row wrap>
                                            <v-flex xs2 md2>s:</v-flex>
                                            <v-flex xs10 md10>
                                              (<BigIntLabel :mpzValue="shuffleProof[1][0]"></BigIntLabel>,
                                              <BigIntLabel :mpzValue="shuffleProof[1][1]"></BigIntLabel>,
                                              <BigIntLabel :mpzValue="shuffleProof[1][2]"></BigIntLabel>,
                                              <BigIntLabel :mpzValue="shuffleProof[1][3]"></BigIntLabel>,
                                              <TupleLabel :tupleValue="shuffleProof[1][4]"></TupleLabel>,
                                              <TupleLabel :tupleValue="shuffleProof[1][5]"></TupleLabel>)
                                            </v-flex>
                                        </v-layout>
                                        <v-layout row wrap>
                                            <v-flex xs2 md2 v-t="'BulletinBoard.commitments_c'"></v-flex>
                                            <v-flex xs10 md10>
                                              <span v-for="c in shuffleProof[2]">
                                                <p><BigIntLabel :mpzValue="c"></BigIntLabel></p>
                                              </span>
                                            </v-flex>
                                        </v-layout>
                                        <v-layout row wrap>
                                            <v-flex xs2 md2 v-t="'BulletinBoard.commitments_c_hat'"></v-flex>
                                            <v-flex xs10 md10>
                                              <span v-for="c_hat in shuffleProof[3]">
                                                <p><BigIntLabel :mpzValue="c_hat"></BigIntLabel></p>
                                              </span>
                                            </v-flex>
                                        </v-layout>
                                    </v-card-text>
                                </v-card>
                            </v-expansion-panel-content>
                        </v-expansion-panel>
                    </DataCard>
                </v-flex>
                <v-flex xy12 md12>
                    <DataCard :title="$t('decryption_proofs')" :tooltip="$t('decryption_proofs_tooltip')" :expandable=false confidentiality="public">
                        <v-expansion-panel class="expansion-panel--popout">
                            <v-expansion-panel-content v-for="(decryptionProof, index) in decryptionProofs" :key="index">
                                <div slot="header">{{ $t('BulletinBoard.decryption_proofs_of_election_authority', { a: index + 1 }) }}</div>
                                <v-card>
                                    <v-card-text class="grey lighten-3">
                                        <v-layout row wrap>
                                            <v-flex xs2 md2>t:</v-flex>
                                            <v-flex xs10 md10>
                                                (<BigIntLabel :mpzValue="decryptionProof[0][0]"></BigIntLabel>,
                                                (<template v-for="t in decryptionProof[0][1]">
                                                    <BigIntLabel :mpzValue="t"></BigIntLabel>,
                                                </template>))
                                            </v-flex>
                                        </v-layout>
                                        <v-layout row wrap>
                                            <v-flex xs2 md2>s:</v-flex>
                                            <v-flex xs10 md10>
                                                <BigIntLabel :mpzValue="decryptionProof[1]"></BigIntLabel>
                                            </v-flex>
                                        </v-layout>
                                    </v-card-text>
                                </v-card>
                            </v-expansion-panel-content>
                        </v-expansion-panel>
                    </DataCard>
                </v-flex>
            </v-layout>
            <ElectionResult v-if="status >= 7"></ElectionResult>
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
    showCredentials: false
  }),
  computed: {
    ...mapState({
      voters: state => state.BulletinBoard.voters,
      countingCircles: state => state.BulletinBoard.countingCircles,
      numberOfCandidates: state => state.BulletinBoard.numberOfCandidates,
      numberOfParallelElections: state => state.BulletinBoard.numberOfParallelElections,
      numberOfSelections: state => state.BulletinBoard.numberOfSelections,
      candidates: state => state.BulletinBoard.candidates,
      publicKey: state => state.BulletinBoard.publicKey,
      shuffleProofs: state => state.BulletinBoard.shuffleProofs,
      decryptionProofs: state => state.BulletinBoard.decryptionProofs,
      confirmations: state => state.BulletinBoard.confirmations
    }),
    ...mapGetters({
      electionId: 'electionId',
      status: 'status',
      statusText: 'statusText',
      fluidLayout: 'fluidLayout'
    }),
    ballots: {
      get: function () {
        return this.$store.getters.getBallotsAndConfirmations(null)
      }
    }
  }
}
</script>
