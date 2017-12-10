<template>
    <v-layout row wrap>
        <v-flex xy12 md4>
            <DataCard :title="$t('votes')" :expandable=false confidentiality="public">{{ votes }}</DataCard>
        </v-flex>
        <v-flex xy12 md4>
            <DataCard :title="$t('final_results')" :expandable=false confidentiality="public">{{ finalResults }}</DataCard>
        </v-flex>
        <v-flex xy12 md4>
            <DataCard :title="$t('counting_circles')" :expandable=false confidentiality="public">{{ w_bold }}</DataCard>
        </v-flex>
        <v-flex xy12 md12>
            <DataCard :title="$t('final_results')" :expandable=false confidentiality="public">
                <v-layout row wrap >
                    <v-flex xy12 md6 v-for="(results, index) in finalResults" :key="index">
                        <donut-chart :id="`donut${index}`" :data="donutData[index]" colors='[ "#FF6384", "#36A2EB", "#FFCE56" ]' resize="false"></donut-chart>
                    </v-flex>
                </v-layout>
            </DataCard>
        </v-flex>
    </v-layout>
</template>

<script>
    import { mapState, mapGetters } from 'vuex'

    export default {
      data: function () {
        return {
        }
      },
      computed: {
        ...mapGetters({
          electionId: 'electionId',
          status: 'status'
        }),
        ...mapState({
          votes: state => state.ElectionAdministrator.votes,
          w_bold: state => state.ElectionAdministrator.w_bold,
          finalResults: state => state.ElectionAdministrator.finalResults,
          electionCandidates: state => state.BulletinBoard.candidates,
          calcNumberOfCandidates: state => state.BulletinBoard.numberOfCandidates
        }),
        donutData: {
          get: function () {
            let donutData = []
            let candidateOffset = 0
            // loop over all parallel election events
            for (let i in this.finalResults) {
              let electionChartData = []
              for (let resIndex in this.finalResults[i]) {
                electionChartData.push({
                  label: this.electionCandidates[Number(resIndex) + candidateOffset], value: this.finalResults[i][Number(resIndex)]
                })
              }
              candidateOffset = candidateOffset + this.calcNumberOfCandidates[i]
              donutData.push(electionChartData)
            }
            return donutData
          }
        }
      },
      mounted () {
      }
    }
</script>