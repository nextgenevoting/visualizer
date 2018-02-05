<template>
    <transition-group tag="div" name="bounce" :appear="generationTransition">
        <v-layout row wrap :key="selectedAuthorityIndex" v-if="status == 1 && hasGenerationTask">
            <v-flex xs12 sm12>
                <v-card>
                    <v-card-title primary-title>
                        <div>
                            <div class="headline" v-t="'Generation.title'"></div>
                        </div>
                    </v-card-title>
                    <v-card-text>
                        <p>{{$t('Generation.text')}}</p>
                    </v-card-text>

                    <v-card-actions>
                        <v-btn flat color="blue" @click="generate()" >
                            <v-icon left>mdi-key-variant</v-icon>
                            {{ $t('Generation.generate') }}
                        </v-btn>
                        <v-spacer></v-spacer>
                        <v-btn icon @click.native="show = !show">
                            <v-icon>{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
                        </v-btn>
                    </v-card-actions>
                    <v-slide-y-transition>
                        <v-card-text v-show="show">
                            todo: explain the electorate data generation phase
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
        generationTransition: false
      }),
      mounted () {
        this.generationTransition = false
      },
      computed: {
        ...mapGetters({
          status: 'status'
        }),
        selectedAuthorityIndex: {
          get: function () {
            return parseInt(this.$route.params.authid)
          }
        },
        electionAuthority: {
          get: function () {
            return this.$store.getters.getElectionAuthority(this.selectedAuthorityIndex)
          }
        },
        hasGenerationTask: {
          get: function () {
            return this.$store.getters.hasGenerationTask(this.selectedAuthorityIndex)
          }
        }
      },
      methods: {
        generate: function () {
          this.$http.post('generateElectorateData', {
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
