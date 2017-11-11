<template>
    <p>{{ tupleValue.length }}-Tuple
    <v-menu
            offset-x
            :close-on-content-click="false"
            :nudge-width="200"
            v-model="menu"
    >
        <v-btn small flat icon slot="activator" style="margin-left:0px;"> <v-icon>mdi-dots-horizontal</v-icon></v-btn>
        <v-card>
            <v-divider></v-divider>
            <v-card-text>
                <v-list>
                    <v-list-tile-title class="datacardTitle" v-if="tupleValue instanceof Array"><b>{{tupleValue.length}}-Tuple</b></v-list-tile-title>
                    <v-list-tile-title class="datacardValue">{{ tupleValue }}</v-list-tile-title>
                </v-list>
            </v-card-text>

        </v-card>
    </v-menu>
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
              if (self.tupleValue !== undefined && self.tupleValue !== null) { return self.tupleValue.toString().substring(0, 10) } else { return '' }
            }
          }
        }
      },
      props: {
        tupleValue: {
          type: Array,
          required: true
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
p{
    display: inline;
}

.datacardTitle {
    text-transform: uppercase
}

.datacardValue{
    overflow-wrap: break-word;
    word-wrap: break-word;
    white-space: pre-wrap;
    height: auto;
}

</style>