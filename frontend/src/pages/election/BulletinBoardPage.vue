<template>
    <v-container grid-list-md>
        <div v-if="this.$store.state.loaded">
            <ContentTitle icon="mdi-bulletin-board" title="Bulletin Board"></ContentTitle>
            <h5 v-if="status >= 4">Post-Election data</h5>
            <v-layout row wrap v-if="status >= 4">
                <v-flex xy12 md12>
                    <DataCard title="Shuffle proofs" :expandable=false confidentiality="public">
                        <v-expansion-panel>
                            <v-expansion-panel-content v-for="(shuffleProof, index) in shuffleProofs" :key="index">
                                <div slot="header">Shuffleproofs of Election Authority {{ index + 1}}
                                </div>
                                <v-card>
                                    <v-card-text class="grey lighten-3">
                                        <v-layout row>
                                            <v-flex xy2 md2>t:</v-flex>
                                            <v-flex xy10 md10>
                                                    <span v-for="t in shuffleProof[0]">
                                                    <BigIntLabel v-if="t instanceof String" :mpzValue="t"></BigIntLabel>
                                                    <TupleLabel v-if="t instanceof Array" :tupleValue="t"></TupleLabel>
                                                    </span>
                                            </v-flex>
                                        </v-layout>
                                        <v-layout row>
                                            <v-flex xy2 md2>s:</v-flex>
                                            <v-flex xy10 md10>
                                                <TupleLabel :tupleValue="shuffleProof[1]"></TupleLabel>
                                            </v-flex>
                                        </v-layout>
                                        <v-layout row>
                                            <v-flex xy2 md2>Commitments c:</v-flex>
                                            <v-flex xy10 md10>
                                                    <span v-for="c in shuffleProof[2]">
                                                    <p><BigIntLabel :mpzValue="c"></BigIntLabel></p>
                                                    </span>
                                            </v-flex>
                                        </v-layout>
                                        <v-layout row>
                                            <v-flex xy2 md2>Commitments c^:</v-flex>
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
            </v-layout>
            <h5>Pre-Election data</h5>
            <v-layout row wrap>
                <v-flex xy12 md4>
                    <DataCard title="Unique Election Identifier" :expandable=false confidentiality="public">{{electionId}}
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Status" :expandable=false confidentiality="public">{{statusText}}</DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Public Key" :isMpz=true :expandable=false confidentiality="public">
                        <BigIntLabel :mpzValue="publicKey"></BigIntLabel>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Parallel elections" :expandable=false confidentiality="public">{{numberOfParallelElections}}</DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Candidates" :expandable=false confidentiality="public">{{candidates}}</DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Number of candidates" :expandable=false confidentiality="public">{{numberOfCandidates}}</DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Number of selections" :expandable=false confidentiality="public">{{numberOfSelections}}
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Voters" :expandable=false confidentiality="public">{{voters}}</DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Counting Circles" :expandable=false confidentiality="public">{{countingCircles}}
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
      decryptionProofs: state => state.BulletinBoard.decryptionProofs
    }),
    ...mapGetters({
      electionId: 'electionId',
      status: 'status',
      statusText: 'statusText'
    })
  }
}
</script>
