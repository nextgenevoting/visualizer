<template>
    <v-container grid-list-md>
        <div v-if="this.$store.state.loaded">
            <ContentTitle icon="mdi-checkbox-marked-outline" :title="$t('Verifier.title')"></ContentTitle>

            <h5 v-t="'tasks'"></h5>
            <v-layout row wrap>
                <v-flex xs12 sm12>
                    <v-btn flat color="blue" @click="verify()">
                        <v-icon left>mdi-checkbox-marked-outline</v-icon>
                        {{ $t('Verifier.verify') }}
                    </v-btn>
                </v-flex>
            </v-layout>
            <h5 v-t="'data'"></h5>
            <v-layout row wrap>
                <v-flex xs12 sm12>
                    <v-card v-if="verificationResult">
                        <v-card-title primary-title>
                            <div>
                                <div class="headline" v-t="'Verifier.task'"></div>
                            </div>
                        </v-card-title>
                        <v-card-text v-if="verificationResult">
                            <v-list two-line>
                                <v-list-tile>
                                    <v-list-tile-content>
                                        <v-list-tile-title v-t="'shuffle_proofs'"></v-list-tile-title>
                                        <v-list-tile-sub-title v-t="'Verifier.shuffle_proofs_description'"></v-list-tile-sub-title>
                                    </v-list-tile-content>
                                    <v-list-tile-action>
                                        <v-icon v-if="verificationResult.shuffleProofsCheck" color="green darken-2">mdi-check-circle-outline</v-icon>
                                        <v-icon v-else color="red">mdi-close-circle-outline</v-icon>
                                    </v-list-tile-action>
                                </v-list-tile>
                                <v-list-tile>
                                    <v-list-tile-content>
                                        <v-list-tile-title v-t="'shuffle_list_dimensions'"></v-list-tile-title>
                                        <v-list-tile-sub-title v-t="'Verifier.shuffle_list_dimensions_description'"></v-list-tile-sub-title>
                                    </v-list-tile-content>
                                    <v-list-tile-action>
                                        <v-icon v-if="verificationResult.shuffleDimensionCheck" color="green darken-2">mdi-check-circle-outline</v-icon>
                                        <v-icon v-else color="red">mdi-close-circle-outline</v-icon>
                                    </v-list-tile-action>
                                </v-list-tile>
                                <v-list-tile>
                                    <v-list-tile-content>
                                        <v-list-tile-title v-t="'decryption_proofs'"></v-list-tile-title>
                                        <v-list-tile-sub-title v-t="'Verifier.decryption_proofs_description'"></v-list-tile-sub-title>
                                    </v-list-tile-content>
                                    <v-list-tile-action>
                                        <v-icon v-if="verificationResult.decryptionProofsCheck" color="green darken-2">mdi-check-circle-outline</v-icon>
                                        <v-icon v-else color="red">mdi-close-circle-outline</v-icon>
                                    </v-list-tile-action>
                                </v-list-tile>

                                <v-list-tile>
                                    <v-list-tile-content>
                                        <v-list-tile-title v-t="'Verifier.other_checks'"></v-list-tile-title>
                                        <v-list-tile-sub-title v-t="'Verifier.other_checks'"></v-list-tile-sub-title>
                                    </v-list-tile-content>
                                    <v-list-tile-action>
                                        Not yet implemented
                                    </v-list-tile-action>
                                </v-list-tile>
                            </v-list>
                        </v-card-text>

                    </v-card>
                </v-flex>
            </v-layout>

        </div>
        <div v-else>
            <LoadingOverlay></LoadingOverlay>
        </div>
    </v-container>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import joinRoomMixin from '../../mixins/joinRoomMixin.js'

export default {
  mixins: [joinRoomMixin],
  data: () => ({
    showCredentials: false
  }),
  computed: {
    ...mapState({
      verificationResult: state => state.BulletinBoard.verificationResult
    }),
    ...mapGetters({
      electionId: 'electionId'
    })
  },
  methods: {
    verify: function () {
      this.$http.post('verifyElection', {
        'election': this.$route.params['electionId']
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
