<template>
    <p>{{ data.truncatedValue() }}
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
                    <v-list-tile-title style=" overflow-wrap: break-word; word-wrap: break-word; white-space: pre-wrap; height: auto;">Size:</v-list-tile-title>

                    <v-list-tile-title style=" overflow-wrap: break-word; word-wrap: break-word; white-space: pre-wrap; height: auto;">{{ mpzValue }}</v-list-tile-title>
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
              if (self.mpzValue !== undefined && self.mpzValue !== null) { return self.mpzValue.toString().substring(0, 10) } else { return '' }
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

      mounted () {
      }
    }
</script>

<style>
p{
    display: inline;
}
</style>