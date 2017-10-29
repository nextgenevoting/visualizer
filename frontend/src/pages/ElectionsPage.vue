<template>
  <v-container>
    <h2 v-t="'title'"></h2>
    <p v-t="'choose'"></p>

    <v-list two-line subheader>
      <v-list-tile v-for="item in getElections" v-bind:key="item.title" avatar
          :to="{ name: 'electionoverview', params: { id: item.id } }">
        <v-list-tile-avatar>
          <v-icon :class="[item.iconClass]">{{ item.icon }}</v-icon>
        </v-list-tile-avatar>

        <v-list-tile-content>
          <v-list-tile-title>{{ item.title }}</v-list-tile-title>
          <v-list-tile-sub-title>{{ item.subtitle }}</v-list-tile-sub-title>
        </v-list-tile-content>

        <v-list-tile-action>
          <v-btn icon @click.prevent="info">
            <v-icon class="grey--text text--lighten-1" :title="$t('info')">info</v-icon>
          </v-btn>
        </v-list-tile-action>

        <v-list-tile-action>
          <v-btn icon @click.prevent="dialog.election = item.id; dialog.visible = true">
            <v-icon class="grey--text text--lighten-1" :title="$t('remove.title')">delete</v-icon>
          </v-btn>
        </v-list-tile-action>
      </v-list-tile>
    </v-list>

    <v-dialog v-model="dialog.visible">
      <v-card>
        <v-card-title class="headline" v-t="'remove.question'" />
        <v-card-actions>
          <v-spacer />
          <v-btn flat color="darken-1" @click.native="dialog.visible = false" v-t="'remove.cancel'" />
          <v-btn flat color="red darken-1" @click.native="remove" v-t="'remove.action'" />
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-btn to="newElection" v-t="'create'" />
  </v-container>
</template>

<i18n>
en:
  title: Available election events
  choose: Please choose an election event.
  create: Create new election
  info: Show information on this election
  remove:
    question: Would you like to delete this election?
    title: Delete election
    action: Delete
    cancel: Cancel
de:
  title: Verfügbare Wahlereignisse
  choose: Bitte wählen Sie ein Wahlereignis aus.
  create: Neue Wahl erstellen
  info: Informationen üver diese Wahl anzeigen
  remove:
    question: Wollen Sie diese Wahl löschen?
    title: Wahl löschen
    action: Löschen
    cancel: Abbrechen
</i18n>

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
    getElections: function () {
      var elections = []

      this.$store.state.Election.elections.forEach((el) => {
        elections.push({
          id:        el._id.$oid,
          icon:      'assignment',
          iconClass: 'blue white--text',
          title:     el.title,
          subtitle:  'Jan 20, 2018'
        })
      })

      return elections
    }
  },
  methods: {
    info () {
      console.log('info')
    },
    remove () {
      this.dialog.visible = false
      console.log('delete ' + this.dialog.election) // TODO
    }
  }
}
</script>
