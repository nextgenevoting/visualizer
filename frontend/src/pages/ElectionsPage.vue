<template>
  <v-container>
    <h2 class="my-3" v-t="'electionsPage.title'"></h2>
    <v-btn to="newElection" style="margin-bottom: 20px">{{ $t('electionsPage.create') }}</v-btn>

    <v-list two-line v-if="elections.length > 0">
      <div v-for="(election, index) in elections" :key="election.id">
        <v-list-tile avatar :to="{ name: 'electionoverview', params: { electionId: election.id } }">
          <v-list-tile-avatar>
            <v-icon class="blue white--text">assignment</v-icon>
          </v-list-tile-avatar>

          <v-list-tile-content>
            <v-list-tile-title>{{ election.title }}</v-list-tile-title>
            <v-list-tile-sub-title>{{ election.subtitle }}</v-list-tile-sub-title>
          </v-list-tile-content>

          <v-list-tile-action>
            <v-btn icon @click.prevent="dialog.election = election; dialog.visible = true">
              <v-icon class="grey--text text--lighten-1" :title="$t('electionsPage.remove.title')">delete</v-icon>
            </v-btn>
          </v-list-tile-action>
        </v-list-tile>
      </div>
    </v-list>

    <v-dialog v-model="dialog.visible">
      <v-card>
        <v-card-title class="headline">{{ $t('electionsPage.remove.question') }}</v-card-title>
        <v-card-actions>
          <v-spacer />
          <v-btn flat color="darken-1" @click.native="dialog.visible = false">{{ $t('cancel') }}</v-btn>
          <v-btn flat color="red darken-1" @click.native="remove">{{ $t('delete') }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-btn to="newElection" v-if="elections.length > 0" style="margin-top: 20px">{{ $t('electionsPage.create') }}</v-btn>
  </v-container>
</template>

<script>
export default {
  data () {
    return {
      dialog: {
        election: null,
        visible: false
      }
    }
  },
  computed: {
    elections () {
      var elections = []

      this.$store.state.Election.elections.forEach((election) => {
        election.id = election._id.$oid
        election.subtitle = 'Jan 20, 2018'
        elections.push(election)
      })

      return elections
    }
  },
  methods: {
    remove () {
      this.dialog.visible = false
      this.$http.delete('deleteElection/' + this.dialog.election.id).then(response => {
        this.$toasted.success(this.$i18n.t('electionsPage.remove.success'))
      }).catch(e => {
        this.$toasted.error(e.body.message)
      })
    }
  }
}
</script>
