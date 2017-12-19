<template>
    <p>
        <span v-if="title === undefined">{{ tupleValue.length }}-Tuple</span>
        <span v-else>{{title}}</span>

    <v-btn v-popover="{ name: data.name }" small flat icon style="margin-left:0px;">
        <v-icon v-if="icon === undefined">mdi-dots-horizontal</v-icon>
        <v-icon v-else>{{icon}}</v-icon>
    </v-btn>

    <popover :name="data.name">
      <div>
                <b v-if="popupTitle === undefined">{{tupleValue.length}}-Tuple</b>
                <b v-else>{{popupTitle}}</b>
      </div>
      <TupleElement :tupleElement="tupleValue" />
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

<style>
    p {
        display: inline;
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
