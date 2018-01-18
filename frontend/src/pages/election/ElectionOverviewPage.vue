<template>
  <v-container :fluid="fluidLayout">
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
        <object type="image/svg+xml" data="/public/parties-overview.svg" ref="svg" style="width: 70%; max-height: 600px">
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
      electionAdministrator: { fill: [ 'path4246' ] },
      bulletinBoard: { fill: [ 'path7835' ] },
      votingClient: { fill: [ 'g6318' ] },
      electionAuthorities: { fill: [ 'path4326' ] },
      printingAuthority: { fill: [ 'path7769' ] },
      voter: { fill: [ 'path7781' ] },
      electionAdministrator_bulletinBoard: { fill: [ 'path3822-6' ], stroke: [ 'path3822-6' ] },
      bulletinBoard_votingClient: { fill: [ 'path3806-5' ], stroke: [ 'path3806-5' ] },
      bulletinBoard_electionAuthorities: { fill: [ 'path3806' ], stroke: [ 'path3806' ] },
      bulletinBoard_printingAuthority: { fill: [ 'path3822' ], stroke: [ 'path3822' ] },
      votingClient_voter: { fill: [ 'path3838', 'path4392' ], stroke: [ 'path3838' ] },
      electionAuthorities_printingAuthority: { fill: [ 'path3884-7', 'path4140' ], stroke: [ 'path3884-7' ] },
      printingAuthority_voter: { fill: [ 'path3884', 'path4140-6' ], stroke: [ 'path3884' ] }
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
      status: 'status',
      fluidLayout: 'fluidLayout'
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

        Object.entries(this.svgElements).forEach(([name, elements]) => {
          let color = active.includes(name) ? 'rgb(38, 132, 192)' : '#000'

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
  mounted () {
    this.checkSVG()
  },
  updated () {
    this.checkSVG()
  },
  watch: {
    status () {
      this.updateSVG()
    }
  }
}
</script>
