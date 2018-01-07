<template>
    <transition-group tag="div" name="bounce" :appear="decryptionTransition">
        <v-layout row wrap :key="selectedAuthorityIndex" v-if="status == 5 && hasDecryptionTask">
            <v-flex xs12 sm12>
                <v-card>
                    <v-card-title primary-title>
                        <div>
                            <div class="headline" v-t="'Decryption.title'"></div>
                        </div>
                    </v-card-title>
                    <v-card-text>
                        <p>{{$t('ElectionAuthority.decryption_text')}}</p>
                        <li v-for="(decryption, index) in decryptions">
                            <BigIntLabel :mpzValue="decryption"></BigIntLabel>
                        </li>
                    </v-card-text>

                    <v-card-actions>
                        <v-btn flat color="blue" @click="decrypt()" >
                            <v-icon left>mdi-key-variant</v-icon>
                            {{ $t('Decryption.decrypt') }}
                        </v-btn>
                        <v-spacer></v-spacer>
                        <v-btn icon @click.native="show = !show">
                            <v-icon>{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
                        </v-btn>
                    </v-card-actions>
                    <v-slide-y-transition>
                        <v-card-text v-show="show">
                            todo: infos about the decryption process
                        </v-card-text>
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
        decryptionTransition: false
      }),
      mounted () {
        this.decryptionTransition = false
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
        decryptions: {
          get: function () {
            return this.$store.getters.getDecryptionsForAuthority(this.selectedAuthorityIndex)
          }
        },
        hasDecryptionTask: {
          get: function () {
            return this.$store.getters.hasDecryptionTask(this.selectedAuthorityIndex)
          }
        }
      },
      methods: {
        decrypt: function () {
          this.$http.post('decrypt', {
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



</style>
