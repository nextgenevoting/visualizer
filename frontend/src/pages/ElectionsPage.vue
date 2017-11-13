<template>
  <v-container>
    <h3 class="my-3" v-t="'electionsPage.title'"></h3>
    <p v-t="'electionsPage.choose'"></p>

    <v-list two-line subheader>
      <v-list-tile v-for="item in getElections" v-bind:key="item.title" avatar
          :to="{ name: 'electionoverview', params: { electionId: item.id } }">
        <v-list-tile-avatar>
          <v-icon :class="[item.iconClass]">{{ item.icon }}</v-icon>
        </v-list-tile-avatar>

        <v-list-tile-content>
          <v-list-tile-title>{{ item.title }}</v-list-tile-title>
          <v-list-tile-sub-title>{{ item.subtitle }}</v-list-tile-sub-title>
        </v-list-tile-content>

        <v-list-tile-action>
          <v-btn icon @click.prevent="info">
            <v-icon class="grey--text text--lighten-1" :title="$t('electionsPage.info')">info</v-icon>
          </v-btn>
        </v-list-tile-action>

        <v-list-tile-action>
          <v-btn icon @click.prevent="dialog.election = item.id; dialog.visible = true">
            <v-icon class="grey--text text--lighten-1" :title="$t('electionsPage.remove.title')">delete</v-icon>
          </v-btn>
        </v-list-tile-action>
      </v-list-tile>
    </v-list>

    <v-dialog v-model="dialog.visible">
      <v-card>
        <v-card-title class="headline" v-t="'electionsPage.remove.question'" />
        <v-card-actions>
          <v-spacer />
          <v-btn flat color="darken-1" @click.native="dialog.visible = false">{{ $t('remove.cancel') }}</v-btn>
          <v-btn flat color="red darken-1" @click.native="remove">{{ $t('delete') }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-btn to="newElection">{{ $t('electionsPage.create') }}</v-btn>
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
    getElections: function () {
      var elections = []

      this.$store.state.Election.elections.forEach((el) => {
        elections.push({
          id: el._id.$oid,
          icon: 'assignment',
          iconClass: 'blue white--text',
          title: el.title,
          subtitle: 'Jan 20, 2018'
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
