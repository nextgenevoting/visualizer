<template>
  <v-container>
    <div v-if="this.$store.state.loaded">
      <ContentTitle icon="mdi-view-dashboard" :title="$t('overview')"></ContentTitle>
      <v-flex xy12 md12>
        <v-stepper color="blue" alt-labels :value="status + 1">
          <v-stepper-header>
            <v-stepper-step step="1" :complete="status >= 1">{{ $t('ElectionStatus.status_1') }}</v-stepper-step>
            <v-divider />
            <v-stepper-step step="2" :complete="status >= 2">{{ $t('ElectionStatus.status_2') }}</v-stepper-step>
            <v-divider />
            <v-stepper-step step="3" :complete="status >= 3">{{ $t('ElectionStatus.status_3') }}</v-stepper-step>
            <v-divider />
            <v-stepper-step step="4" :complete="status >= 4">{{ $t('ElectionStatus.status_4') }}</v-stepper-step>
            <v-divider />
            <v-stepper-step step="5" :complete="status >= 5">{{ $t('ElectionStatus.status_5') }}</v-stepper-step>
            <v-divider />
            <v-stepper-step step="6" :complete="status >= 6">{{ $t('ElectionStatus.status_6') }}</v-stepper-step>
            <v-divider />
            <v-stepper-step step="7" :complete="status >= 7">{{ $t('ElectionStatus.status_7') }}</v-stepper-step>
          </v-stepper-header>
        </v-stepper>
      </v-flex>

      <div style="text-align: center; margin-top: 50px;">
        <object type="image/svg+xml" data="/public/parties-overview.svg" ref="svg" style="width: 70%;">
          Your browser does not support SVGs
        </object>
      </div>
    </div>
    <div v-else>
      <LoadingOverlay></LoadingOverlay>
    </div>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import joinRoomMixin from '../../mixins/joinRoomMixin.js'

export default {
  data: () => ({
    svg: null,
    svgElements: {
      electionAdministrator: { fill: [ 'g3410', 'path4246' ] },
      bulletinBoard: { fill: [ 'g3546' ] },
      votingClient: { fill: [ 'g3726' ] },
      electionAuthorities: { fill: [ 'g3612', 'path4326' ] },
      printingAuthority: { fill: [ 'g3478' ] },
      voter: { fill: [ 'path3724', 'path3722' ] },
      electionAdministrator_bulletinBoard: { fill: [ 'path3802', 'path3796' ], stroke: [ 'path3806', 'path3794', 'path3800' ] },
      bulletinBoard_votingClient: { fill: [ 'path3850', 'path3844' ], stroke: [ 'path3854', 'path3842', 'path3848' ] },
      bulletinBoard_electionAuthorities: { fill: [ 'path3812', 'path3818' ], stroke: [ 'path3816', 'path3810', 'path3822' ] },
      bulletinBoard_printingAuthority: { fill: [ 'path3870' ], stroke: [ 'path3868', 'path3874' ] },
      votingClient_voter: { fill: [ 'path4392', 'path3834', 'path3828' ], stroke: [ 'path3838', 'path3826', 'path3832' ] },
      electionAuthorities_printingAuthority: { fill: [ 'path4140', 'path3860' ], stroke: [ 'path3858', 'path3864' ] },
      printingAuthority_voter: { fill: [ 'path4074', 'path3880' ], stroke: [ 'path3878', 'path3884' ] }
    },
    svgStates: {
      0: [ 'electionAdministrator', 'electionAdministrator_bulletinBoard', 'bulletinBoard', 'bulletinBoard_printingAuthority' ], // Preparation
      1: [ 'printingAuthority' ], // Printing
      2: [ 'printingAuthority', 'printingAuthority_voter', 'voter' ], // Delivery
      3: [ 'voter', 'votingClient_voter', 'votingClient', 'bulletinBoard_votingClient', 'bulletinBoard' ], // Election Phase
      4: [ 'electionAuthorities', 'bulletinBoard_electionAuthorities', 'bulletinBoard' ], // Mixing Phase
      5: [ 'electionAuthorities', 'bulletinBoard_electionAuthorities', 'bulletinBoard' ], // Decryption Phase
      6: [ 'electionAdministrator', 'electionAdministrator_bulletinBoard', 'bulletinBoard' ] // Tallying Phase
    }
  }),
  mixins: [joinRoomMixin],
  computed: {
    ...mapGetters({
      electionId: 'electionId',
      statusText: 'statusText',
      status: 'status'
    })
  },
  methods: {
    checkSVG () {
      if (this.$refs.hasOwnProperty('svg')) {
        this.$refs.svg.addEventListener('load', () => {
          this.svg = this.$refs.svg.contentDocument
          this.updateSVG()
        })
      }
    },
    updateSVG () {
      if (this.svg !== null) {
        let active = this.svgStates.hasOwnProperty(this.status) ? this.svgStates[this.status] : []
        console.log(active)

        Object.entries(this.svgElements).forEach(([name, elements]) => {
          let color = active.includes(name) ? 'rgb(38, 132, 192)' : '#000'

          console.log(name, color)

          if (elements.hasOwnProperty('fill')) {
            elements.fill.forEach((id) => {
              this.svg.getElementById(id).setAttribute('fill', color)
            })
          }

          if (elements.hasOwnProperty('stroke')) {
            elements.stroke.forEach((id) => {
              this.svg.getElementById(id).style.stroke = color
            })
          }
        })
      }
    }
  },
  updated () {
    this.checkSVG()
  },
  mounted () {
    this.checkSVG()
  },
  watch: {
    // status: () => {
    //   this.updateSVG()
    // }
  }
}
</script>

<style scoped>
</style>
