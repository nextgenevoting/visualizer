<template>
    <v-card class="dataCard">

        <span v-if="data.showConfidentiality" tabindex="0" class="ml-0 chip chip--label chip--small lighten-4 confidentiallyChip" v-bind:class="confidentiality == 'secret' ? 'red' : (confidentiality == 'encrypted' ? 'yellow' : 'green')">{{confidentiality}}</span>


        <v-card-title primary-title class="dataCardTitle">
            <div><span class="label grey--text">{{title}}
              <v-tooltip top>
                <v-icon v-if="!disableTooltip" color="grey lighten-1" slot="activator">info</v-icon><span>Programmatic tooltip</span>
             </v-tooltip></span>
            </div>
        </v-card-title>
        <v-card-text class="dataCardContent">
                <slot></slot>

        </v-card-text>
        <v-card-actions style="height:33px; padding: 0px" v-show="expandable">

            <v-spacer></v-spacer>
            <v-btn icon @click.native="showExpander = !showExpander">
                <v-icon>{{ !showExpander ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
            </v-btn>
        </v-card-actions>
        <v-slide-y-transition v-show="expandable">
            <v-card-text v-show="showExpander">
                <slot name="expandContent">
                </slot>
            </v-card-text>
        </v-slide-y-transition>
    </v-card>
</template>

<script>
    export default {
      data: function () {
        return {
          showExpander: false
        }
      },
      computed: {
        data () {
          return {
            showConfidentiality: this.$store.state.showConfidentiality
          }
        }
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
        }

      },

      mounted () {
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

    .confidentiallyChip {
        position: absolute;
        top: 7px;
        right: 7px;
    }
</style>