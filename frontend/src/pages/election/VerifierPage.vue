<template>
    <v-container grid-list-md>
        <div v-if="this.$store.state.loaded">
            <ContentTitle icon="mdi-checkbox-marked-outline" :title="$t('Verifier.title')"></ContentTitle>

            <h5 v-t="'BulletinBoard.pre_election_data'"></h5>
            <v-layout row wrap>
                <v-flex xy12 md4>
                    <DataCard :title="$t('BulletinBoard.unique_election_identifier')" :expandable=false confidentiality="public">{{ electionId }}</DataCard>
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
      voters: state => state.BulletinBoard.voters
    }),
    ...mapGetters({
      electionId: 'electionId'
    }),
    ballots: {
      get: function () {
        return this.$store.getters.getBallotsAndConfirmations(null)
      }
    }
  }
}
</script>
