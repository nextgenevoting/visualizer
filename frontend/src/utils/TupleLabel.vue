<template>
    <p >
        <span v-if="title === undefined">{{ tupleValue.length }}-Tuple</span>
        <span v-else>{{title}}</span>

    <v-btn v-popover="{ name: name }" small flat icon style="margin-left:0px;">
        <v-icon v-if="icon === undefined">mdi-dots-horizontal</v-icon>
        <v-icon v-else>{{icon}}</v-icon>
    </v-btn>
    <popover :name="name">

        <v-list>
            <v-list-tile-title class="datacardTitle" v-if="tupleValue instanceof Array">
                <b>{{tupleValue.length}}-Tuple</b></v-list-tile-title>
            <v-list-tile-title class="datacardValue">
                <div v-for="(v, index) in tupleValue">
                    <p><b>{{index+1}}:</b>{{ v }}</p>
                </div>
            </v-list-tile-title>
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
              if (self.tupleValue !== undefined && self.tupleValue !== null) {
                return self.tupleValue.toString().substring(0, 10)
              } else {
                return ''
              }
            }
          }
        }
      },
      props: {
        tupleValue: {
          type: Array,
          required: true
        },
        name: {
          type: String,
          requried: true
        },
        title: {
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
      },
      mounted () {
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