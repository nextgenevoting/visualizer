<template>
    <transition-group tag="div" name="" :appear="mixingTransition">
        <v-layout row  v-if="encryptions.length > 0" :key="selectedAuthorityIndex">
            <v-flex xs12 sm12>
                <v-card>
                    <v-card-title primary-title>
                        <div>
                            <div class="headline">Mixing Task</div>
                        </div>
                    </v-card-title>
                    <v-card-text>
                        <p>Every election authority must now shuffle the list of encryptions</p>
                        <transition-group name="flip-list" tag="ul">
                            <li v-for="(encryption, index) in encryptions" v-bind:key="encryption.key">
                                <BigIntLabel :mpzValue="encryption.a"></BigIntLabel>, <BigIntLabel :mpzValue="encryption.b"></BigIntLabel>

                            </li>
                        </transition-group>
                    </v-card-text>

                    <v-card-actions>
                        <v-btn flat color="blue" @click="mix()" :disabled="electionAuthority.encryptionsShuffled.length > 0">
                            <v-icon left>mdi-shuffle-variant</v-icon>
                            Shuffle encryptions
                        </v-btn>
                        <v-spacer></v-spacer>
                        <v-btn icon @click.native="show = !show">
                            <v-icon>{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
                        </v-btn>
                    </v-card-actions>
                    <v-slide-y-transition>
                        <v-card-text v-show="show">
                            todo: infos about the mixing process
                        </v-card-text>
                    </v-slide-y-transition>
                </v-card>
            </v-flex>
        </v-layout>
    </transition-group>
</template>

<script>
    export default {
      data: () => ({
        show: false,
        mixingTransition: false
      }),
      mounted () {
        this.mixingTransition = false
      },
      computed: {
        selectedAuthorityIndex: {
          get: function () {
            return parseInt(this.$route.params.authid)
          },
          set: function (newAuthId) {
            this.$store.commit('selectedAuthority', newAuthId)
            this.$router.push({name: 'electionauthority', params: {electionId: this.$route.params['electionId'], authid: newAuthId}})
          }
        },
        electionAuthority: {
          get: function () {
            return this.$store.getters.getElectionAuthority(this.selectedAuthorityIndex)
          }
        },
        encryptions: {
          get: function () {
            return this.$store.getters.getEncryptionsForAuthority(this.selectedAuthorityIndex)
          }
        }
      },
      methods: {
        mix: function () {
          this.$http.post('mix', {
            'election': this.$route.params['electionId'],
            'authorityId': this.selectedAuthorityIndex
          }).then(response => {
            response.json().then((data) => {
              // success callback
              // this.$toasted.success('Successfully checked confirmation')
            })
          }).catch(e => {
            this.$toasted.error(e.body.message)
          })
        }

      }
    }
</script>

<style>

    .flip-list-move {
        transition: transform 1.3s;
    }

    .bounce-enter-active {
        animation: bounce-in .5s;
    }

    .bounce-leave-active {
        animation: bounce-in .4s reverse;
    }

    @keyframes bounce-in {
        0% {
            transform: scale(0);
            opacity: 0;
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }
</style>