<template>
    <v-container grid-list-md>
        <div v-if="this.$store.state.loaded">
            <ContentTitle icon="mdi-bulletin-board" :title="$t('BulletinBoard.title')"></ContentTitle>

            <h5 v-t="'BulletinBoard.pre_election_data'"></h5>
            <v-layout row wrap>
                <v-flex xy12 md4>
                    <DataCard :title="$t('BulletinBoard.unique_election_identifier')" :expandable=false confidentiality="public">{{ electionId }}</DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard :title="$t('status')" :expandable=false confidentiality="public">{{ statusText }}</DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard :title="$t('public_key')" :isMpz=true :expandable=false confidentiality="public">
                        <BigIntLabel :mpzValue="publicKey"></BigIntLabel>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard :title="$t('BulletinBoard.parallel_elections')" :expandable=false confidentiality="public">{{ numberOfParallelElections }}</DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard :title="$t('candidates')" :expandable=false confidentiality="public">
                        <template v-for="(candidate, index) in candidates">
                            {{candidate}}<span v-if="index < candidates.length-1">, </span>
                        </template>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard :title="$t('number_of_candidates')" :expandable=false confidentiality="public">
                        <template v-for="(candidates, index) in numberOfCandidates">
                            {{candidates}}<span v-if="index < numberOfCandidates.length-1">, </span>
                        </template>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard :title="$t('number_of_selections')" :expandable=false confidentiality="public">
                        <template v-for="(k, index) in numberOfSelections">
                            {{k}}<span v-if="index < numberOfSelections.length-1">, </span>
                        </template>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard :title="$t('voters')" :expandable=false confidentiality="public">
                        <template v-for="(v, index) in voters">
                            {{v}}<span v-if="index < voters.length-1">, </span>
                        </template>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard :title="$t('counting_circles')" :expandable=false confidentiality="public">
                        <template v-for="(c, index) in countingCircles">
                            {{c}}<span v-if="index < countingCircles.length-1">, </span>
                        </template>
                    </DataCard>
                </v-flex>


            </v-layout>

            <h5 v-if="status >= 3" v-t="'election_data'"></h5>
            <v-layout row wrap>
                <v-flex xy12 md12>
                    <DataCard :title="$t('ballots')" :expandable=false confidentiality="encrypted">
                        <BallotList :ballots="ballots"></BallotList>
                    </DataCard>
                </v-flex>

            </v-layout>


            <h5 v-if="status >= 4" v-t="'post_election_data'"></h5>
            <v-layout row wrap v-if="status >= 4">
                <v-flex xy12 md12>
                    <DataCard title="Shuffle proofs" :expandable=false confidentiality="public">
                        <v-expansion-panel class="expansion-panel--popout">
                            <v-expansion-panel-content v-for="(shuffleProof, index) in shuffleProofs" :key="index">
                                <div slot="header">{{ $t('BulletinBoard.shuffle_proofs_of_election_authority', { a: index + 1 }) }}</div>
                                <v-card>
                                    <v-card-text class="grey lighten-3">
                                        <v-layout row wrap>
                                            <v-flex xy2 md2>t:</v-flex>
                                            <v-flex xy10 md10>
                                                    (<BigIntLabel :mpzValue="shuffleProof[0][0]"></BigIntLabel>,
                                                    <BigIntLabel :mpzValue="shuffleProof[0][1]"></BigIntLabel>,
                                                    <BigIntLabel :mpzValue="shuffleProof[0][2]"></BigIntLabel>,
                                                    <TupleLabel :tupleValue="shuffleProof[0][3]"></TupleLabel>,
                                                    <TupleLabel :tupleValue="shuffleProof[0][4]"></TupleLabel>)
                                            </v-flex>
                                        </v-layout>
                                        <v-layout row wrap>
                                            <v-flex xy2 md2>s:</v-flex>
                                            <v-flex xy10 md10>
                                                (<BigIntLabel :mpzValue="shuffleProof[1][0]"></BigIntLabel>,
                                                <BigIntLabel :mpzValue="shuffleProof[1][1]"></BigIntLabel>,
                                                <BigIntLabel :mpzValue="shuffleProof[1][2]"></BigIntLabel>,
                                                <BigIntLabel :mpzValue="shuffleProof[1][3]"></BigIntLabel>,
                                                <TupleLabel :tupleValue="shuffleProof[1][4]"></TupleLabel>,
                                                <TupleLabel :tupleValue="shuffleProof[1][5]"></TupleLabel>)
                                            </v-flex>
                                        </v-layout>
                                        <v-layout row wrap>
                                            <v-flex xy2 md2 v-t="'BulletinBoard.commitments_c'"></v-flex>
                                            <v-flex xy10 md10>
                                                    <span v-for="c in shuffleProof[2]">
                                                    <p><BigIntLabel :mpzValue="c"></BigIntLabel></p>
                                                    </span>
                                            </v-flex>
                                        </v-layout>
                                        <v-layout row wrap>
                                            <v-flex xy2 md2 v-t="'BulletinBoard.commitments_c_hat'"></v-flex>
                                            <v-flex xy10 md10>
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
                    <DataCard title="Decryption proofs" :expandable=false confidentiality="public">
                        <v-expansion-panel class="expansion-panel--popout">
                            <v-expansion-panel-content v-for="(decryptionProof, index) in decryptionProofs" :key="index">
                                <div slot="header">{{ $t('BulletinBoard.decryption_proofs_of_election_authority', { a: index + 1 }) }}</div>
                                <v-card>
                                    <v-card-text class="grey lighten-3">
                                        <v-layout row wrap>
                                            <v-flex xy2 md2>t:</v-flex>
                                            <v-flex xy10 md10>
                                                (<BigIntLabel :mpzValue="decryptionProof[0][0]"></BigIntLabel>,
                                                (
                                                <template v-for="t in decryptionProof[0][1]">
                                                    <BigIntLabel :mpzValue="t"></BigIntLabel>,
                                                </template>
                                                ))
                                            </v-flex>
                                        </v-layout>
                                        <v-layout row wrap>
                                            <v-flex xy2 md2>s:</v-flex>
                                            <v-flex xy10 md10>
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
      statusText: 'statusText'
    }),
    ballots: {
      get: function () {
        return this.$store.getters.getBallotsAndConfirmations(null)
      }
    }
  }
}
</script>
