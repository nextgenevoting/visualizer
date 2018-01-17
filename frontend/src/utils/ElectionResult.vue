<template>
    <v-layout row wrap>
        <v-flex xs12 md6>
            <DataCard :title="$t('ElectionResult.votes')" :tooltip="$t('ElectionResult.votes_tooltip')" :expandable=false confidentiality="public" v-if="votes.length > 0">
                <v-data-table
                        v-bind:headers="headers"
                        :items="items"
                        hide-actions
                        class="elevation-0"
                >
                    {{items}}
                    <template slot="items" slot-scope="props">
                        <td>{{ props.item.name }}</td>
                        <td class="text-xs-right">{{ props.item.candidate }}</td>
                        <td class="text-xs-right">{{ props.item.countingCircle }}</td>
                    </template>
                </v-data-table>

            </DataCard>
        </v-flex>
        <v-flex xs12 md6  v-for="(results, index) in finalResults" :key="index">
            <DataCard :title="$t('ElectionResult.final_results', {n: index + 1})" :tooltip="$t('ElectionResult.final_results_tooltip')" :expandable=false confidentiality="public" v-if="finalResults.length > 0">
            <v-layout row wrap>
                <v-flex xs12 md12>
                    <v-data-table
                            v-bind:headers="resultHeaders"
                            :items="electionResults[index]"
                            hide-actions
                            class="elevation-0"
                    >
                        {{items}}
                        <template slot="items" slot-scope="props">
                            <td>{{ props.item.label }}</td>
                            <td class="text-xs-right">{{ props.item.value }}</td>
                        </template>
                    </v-data-table>
                </v-flex>
                <v-flex xs12 md12>
                    <donut-chart :id="`donut${index}`" :data="electionResults[index]" colors='[ "#FF6384", "#36A2EB", "#FFCE56" ]' resize="true"></donut-chart>
                </v-flex>
                </v-layout>
            </DataCard>
        </v-flex>
        <!--<v-flex xy12 md4>
            <DataCard :title="$t('counting_circles')" :tooltip="$t('ElectionResult.counting_circles_tooltip')" :expandable=false confidentiality="public" v-if="countingCircles.length > 0">
                <template v-for="(c,index) in countingCircles">
                    {{ c }}<span v-if="index < countingCircles.length-1">,</span>
                </template>
            </DataCard>
        </v-flex>-->
       <!-- <v-flex xy12 md12>
            <DataCard :title="$t('ElectionResult.final_results_chart')" :tooltip="$t('ElectionResult.final_results_chart_tooltip')" :expandable=false confidentiality="public" v-if="finalResults.length > 0">
                <v-layout row wrap >
                    <v-flex xy12 md6 v-for="(results, index) in finalResults" :key="index">
                        <donut-chart :id="`donut${index}`" :data="electionResults[index]" colors='[ "#FF6384", "#36A2EB", "#FFCE56" ]' resize="false"></donut-chart>
                    </v-flex>
                </v-layout>
            </DataCard>
        </v-flex>-->
    </v-layout>
</template>

<script>
    import { mapState, mapGetters } from 'vuex'

    export default {
      data: function () {
        return {
          headers: [
            {
              text: 'Vote',
              align: 'left',
              sortable: true,
              value: 'name'
            },
            { text: this.$i18n.t('candidate'), value: 'candidate' },
            { text: this.$i18n.t('counting_circle'), value: 'countingCircle' }
          ],
          resultHeaders: [
            {
              text: this.$i18n.t('candidate'),
              align: 'left',
              sortable: true,
              value: 'label'
            },
            { text: this.$i18n.t('num_of_votes'), value: 'value' }
          ]
        }
      },
      computed: {
        ...mapGetters({
          electionId: 'electionId',
          status: 'status'
        }),
        ...mapState({
          votes: state => state.ElectionAdministrator.votes,
          countingCircles: state => state.ElectionAdministrator.w_bold,
          finalResults: state => state.ElectionAdministrator.finalResults,
          electionCandidates: state => state.BulletinBoard.candidates,
          calcNumberOfCandidates: state => state.BulletinBoard.numberOfCandidates
        }),
        items: {
          get: function () {
            let gridData = []
            for (const [index, vote] of this.votes.entries()) {
              gridData.push({
                name: `${index + 1}`,
                candidate: vote.reduce((a, e, i) => (e === 1) ? a.concat(this.electionCandidates[i]) : a, []).join(', '),
                countingCircle: this.countingCircles[index].reduce((a, e, i) => (e === 1) ? a.concat(i) : a, []).join(', ')
              })
            }
            return gridData
          }
        },
        electionResults: {
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