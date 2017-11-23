<template>
    <p>{{ data.truncatedValue() }}

        <v-btn v-popover="{ name: mpzValue }" small flat icon style="margin-left:0px;" @click="clickHeader($event)">
            <v-icon>mdi-dots-horizontal</v-icon>
        </v-btn>
        <popover :name="mpzValue">

            <v-list>
                <v-list-tile-title class="datacardTitle" v-if="isString(mpzValue)"><b>{{ data.bitLength()
                    }}-Bit number</b></v-list-tile-title>
                <v-list-tile-title class="datacardValue">{{ mpzValue }}</v-list-tile-title>
            </v-list>

        </popover>
    </p>


</template>

<script>
    export default {
      data: () => ({
        menu: false
      }),
      computed: {
        data () {
          var self = this
          return {
            truncatedValue: function () {
              if (self.mpzValue !== undefined && self.mpzValue !== null) {
                return self.mpzValue.toString().substring(0, 6)
              } else {
                return ''
              }
            },
            bitLength: function () {
              let digits = 0
              while (self.mpzValue > 2 ** digits) { digits++ }
              return digits
            }
          }
        }
      },
      props: {
        mpzValue: {
          type: String,
          required: true
        }
      },
      methods: {
        isString: function (s) {
          return typeof (s) === 'string' || s instanceof String
        },
        clickHeader: function (event) {
          this.menu = !this.menu
          event.stopPropagation()
        }
      },
      mounted () {
      }
    }
</script>

<style>
    .vue-popover {
        width: 650px !important;
        padding: 15px;

    }

    p {
        display: inline;
    }

    .vue-popover .datacardTitle {
        text-transform: uppercase;
        font-size: 15px;
    }

    .vue-popover .datacardValue {
        overflow-wrap: break-word;
        word-wrap: break-word;
        white-space: pre-wrap;
        height: auto;
        font-size: 14px;
    }

</style>