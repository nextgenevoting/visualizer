<template>
<v-dialog v-model="showDialog" max-width="400px">
    <v-card>
        <v-card-title>
            {{$t('SelectVoterDialog.title')}}
        </v-card-title>
        <v-card-text>
            <v-list>
                <v-list-tile v-for="(voter, index) in this.$store.state.Voter.voters" v-bind:key="voter.id"
                             active-class="default-class your-class"
                             @click="selectVoter(voter.id)">
                    <v-list-tile-content>
                        <v-list-tile-title>{{ voter.name }}</v-list-tile-title>
                    </v-list-tile-content>
                    <v-list-tile-action>
                        <v-icon :class="voter.status < 1 ? 'pending' : ''">mdi-thumbs-up-down</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-action>
                        <v-icon :class="voter.status < 2 ? 'pending' : ''">mdi-checkbox-marked-circle</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-action>
                        <v-icon :class="voter.status < 3 ? 'pending' : ''">mdi-ray-end</v-icon>
                    </v-list-tile-action>

                </v-list-tile>
            </v-list>
        </v-card-text>
        <v-card-actions>
            <v-btn color="primary" flat @click.stop="showDialog=false" v-t="'close'"></v-btn>
        </v-card-actions>
    </v-card>
</v-dialog>
</template>

<script>
    export default {
      data: function () {
        return {
        }
      },
      computed: {
        showDialog: {
          get () {
            return this.$store.state.voterDialog
          },
          set (value) {
            this.$store.commit('voterDialog', value)
          }
        }
      },
      methods: {
        selectVoter: function (id) {
          this.$store.commit('voterDialog', false)
          this.$store.commit('selectedVoter', id)
          this.$router.push({name: 'voter', params: {electionId: this.$route.params['electionId'], voterId: id}})
        }
      },
      created () {
      }
    }
</script>
