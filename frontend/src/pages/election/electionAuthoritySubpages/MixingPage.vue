<template>
    <transition-group tag="div" name="bounce" :appear="mixingTransition">
        <v-layout row wrap v-if="status == 4 && encryptions.length > 0" :key="selectedAuthorityIndex">
            <v-flex xs12 sm12>
                <v-card>
                    <v-card-title primary-title>
                        <div>
                            <div class="headline" v-t="'Mixing.title'"></div>
                        </div>
                    </v-card-title>
                    <v-card-text>
                        <p v-if="!hasAuthorityMixed" v-t="'Mixing.every_election_authority'"></p>
                        <p v-else>{{ $t('Mixing.permutation')}} {{electionAuthority.permutation}}</p>

                        <transition-group name="flip-list" tag="ul" style="margin-top: 10px;">
                            <li v-for="(encryption, index) in encryptions" v-bind:key="encryption.key">
                                <BigIntLabel :mpzValue="encryption.a"></BigIntLabel>, <BigIntLabel :mpzValue="encryption.b"></BigIntLabel>
                            </li>
                        </transition-group>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn flat color="blue" @click="mix()" :disabled="hasAuthorityMixed">
                            <v-icon left>mdi-shuffle-variant</v-icon>
                            {{ $t('Mixing.shuffle_encryptions') }}
                        </v-btn>
                        <v-spacer></v-spacer>

                    </v-card-actions>
                    <v-slide-y-transition>

                    </v-slide-y-transition>
                </v-card>
            </v-flex>
        </v-layout>
    </transition-group>
</template>

<script>
    import { mapGetters } from 'vuex'

    export default {
      data: () => ({
        show: false,
        mixingTransition: false
      }),
      mounted () {
        this.mixingTransition = false
      },
      computed: {
        ...mapGetters({
          status: 'status'
        }),
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
        },
        hasAuthorityMixed: {
          get: function () {
            return this.$store.getters.hasAuthorityMixed(this.selectedAuthorityIndex)
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


</style>
