<template>
    <v-container>
        <h2 v-t="'title'"></h2>
        <p v-t="'choose'"></p>

        <v-list two-line subheader>
            <v-list-tile v-for="item in getElections" v-bind:key="item.title" avatar
                         :to="{ name: 'electionoverview', params: {id: item.id }}">
                <v-list-tile-avatar>
                    <v-icon v-bind:class="[item.iconClass]">{{ item.icon }}</v-icon>
                </v-list-tile-avatar>
                <v-list-tile-content>
                    <v-list-tile-title>{{ item.title }}</v-list-tile-title>
                    <v-list-tile-sub-title>{{ item.subtitle }}</v-list-tile-sub-title>
                </v-list-tile-content>
                <v-list-tile-action>
                    <v-btn icon ripple>
                        <v-icon class="grey--text text--lighten-1">info</v-icon>
                    </v-btn>
                </v-list-tile-action>
            </v-list-tile>
        </v-list>
        <v-btn to="newElection" v-t="'create'"/>
    </v-container>
</template>

<i18n>
en:
  title: Available election events
  choose: Please choose an election event.
  create: Create new
de:
  title: Verfügbare Wahlereignisse
  choose: Bitte wählen Sie ein Wahlereignis aus.
  create: Neue erstellen
</i18n>

<script>
    export default {
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
        mounted() {
        }
    }
</script>
