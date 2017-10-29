<template>
  <v-container grid-list-xl text-xs-center>
    <v-layout row wrap>
      <v-flex xs10 offset-xs1>
        <v-card class="pa-5">
          <span class="headline" v-t="'heading'"/>
          <v-form>
            <v-text-field :label="$t('title')" v-model="title" required />
            <v-btn @click="createElection" v-t="'create'"/>
          </v-form>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<i18n>
en:
  heading: Create new election
  title: Title
  create: Create
de:
  heading: Neue Wahl erstellen
  title: Titel
  create: Erstellen
</i18n>

<script>
export default {
  data () {
    return {
        title: ''
    }
  },
  methods: {
    createElection () {
      //this.$socket.emit('createElection', { title: this.title});
      this.$http.post('createElection', {title: this.title}).then(response => {
        response.json().then((data) => {
          this.$router.push({name: 'electionoverview', params: {id: data.id}});
        })
      }, response => {
          // error callback
      })
    }
  },
  created () {
    this.unsub = this.$store.subscribe((mutation, state) => console.log(mutation));
  },
  beforeDestroy () {
    console.log("before destroy");
    this.unsub();
  }
}
</script>
