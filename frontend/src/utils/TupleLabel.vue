<template>
        <span>{{ tupleValue.length }}-Tuple
        <v-menu offset-y :max-width="600">
            <v-btn small flat icon slot="activator" style="margin-left: 0px; color: rgba(0,0,0,.54)">
                <v-icon>mdi-dots-horizontal</v-icon>
            </v-btn>
                  <v-card>
             <v-card-title  class="subheading" style="padding-bottom: 0px;">
                <b v-if="popupTitle === undefined">{{tupleValue.length}}-Tuple</b>
        </v-card-title>
                          <v-card-text>
          <div class="wrap"><TupleElement class="wrap" :tupleElement="tupleValue"/></div>
        </v-card-text>
                  </v-card>
            <!--
            <div v-for="(value, index) in tupleValue">
                <div v-if="value instanceof Array">
                    <b>{{index+1}}:</b>
                    <div v-for="v in value">
                      <TupleElement :tupleElement="v"></TupleElement>
                    </div>
                </div>
                <div v-else><b>{{index+1}}:</b>{{v}}</div>
            </div>
            -->
            </v-menu>
        </span>

</template>

<script>
    export default {
      data: () => ({
        menu: false
      }),
      computed: {
        data () {
          var self = this
          console.log(this.tupleValue)
          return {
            truncatedValue: function () {
              if (self.tupleValue !== undefined && self.tupleValue !== null) {
                return self.tupleValue.toString().substring(0, 10)
              } else {
                return ''
              }
            },
            name: (function () {
              return String(Math.random())
            }())
          }
        }
      },
      props: {
        tupleValue: {
          type: Array,
          required: true
        },

        title: {
          type: String,
          requried: false
        },
        popupTitle: {
          type: String,
          requried: false
        },
        icon: {
          type: String,
          requried: false
        }

      },
      methods: {
        isString: function (s) {
          return typeof (s) === 'string' || s instanceof String
        }
      }
    }
</script>

<style scoped>
    p {
        display: inline;
    }
    .wrap {
        overflow-wrap: break-word;
        word-wrap: break-word;
        white-space: pre-wrap;
    }
    .vue-popover .datacardTitle {
        text-transform: uppercase;
        font-size: 16px;
    }

    .vue-popover .datacardValue {
        overflow-wrap: break-word;
        word-wrap: break-word;
        white-space: pre-wrap;
        height: auto;
        font-size: 14px;
    }

    .vue-popover {
        width: 650px !important;
        padding: 15px;

    }
</style>
