<template>
  <v-card class="dataCard">
    <ConfidentialityChip :type="confidentiality" class="confidentialityChip" />

    <v-card-title primary-title class="dataCardTitle label grey--text">
      {{ title }}
      <v-tooltip top style="cursor: default">
        <v-icon v-if="!disableTooltip" color="grey lighten-1" slot="activator">info</v-icon>
        <span>{{ tooltip }}</span>
      </v-tooltip>
    </v-card-title>

    <v-card-text class="dataCardContent">
      <slot></slot>
    </v-card-text>

    <v-card-actions style="height:33px; padding: 0px" v-show="expandable">
      <v-spacer />
      <v-btn icon @click.native="showExpander = !showExpander">
          <v-icon>{{ !showExpander ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
      </v-btn>
    </v-card-actions>

    <v-slide-y-transition v-show="expandable">
      <v-card-text v-show="showExpander">
        <slot name="expandContent"></slot>
      </v-card-text>
    </v-slide-y-transition>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data: function () {
    return {
      showExpander: false
    }
  },
  computed: {
    ...mapState({
      voters: state => state.BulletinBoard.voters
    })
  },
  props: {
    title: {
      type: String,
      required: true,
      default: 'Title'
    },
    expandable: {
      type: Boolean,
      required: true,
      default: false
    },
    confidentiality: {
      type: String,
      required: true,
      default: 'public'
    },
    disableTooltip: {
      type: Boolean,
      required: false,
      default: false
    },
    tooltip: {
      type: String,
      required: false,
      default: ''
    }
  }
}
</script>

<style>
p {
    display: inline;
}

.dataCard .dataCardTitle{
    padding: 10px 16px 5px 16px !important;
}

.dataCard .dataCardContent{
    padding: 2px 16px 10px 16px !important;
    font-size: 22px !important;
    min-height: 52px;
}

.confidentialityChip {
    position: absolute;
    top: 7px;
    right: 7px;
}
</style>
