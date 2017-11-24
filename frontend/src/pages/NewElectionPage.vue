<template>
  <v-container grid-list-xl text-xs-center>
    <v-layout row wrap>
      <v-flex xs10 offset-xs1>
        <v-card class="pa-5">
          <span class="headline" v-t="'electionsPage.create'" />
          <v-form @submit.prevent="createElection">
            <v-text-field :label="$t('title')" v-model="title" required />
            <v-btn color="primary" @click="createElection">{{ $t('create') }}</v-btn>
          </v-form>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  data () {
    return {
      title: ''
    }
  },
  methods: {
    createElection () {
      this.$http.post('createElection', { title: this.title }).then(response => {
        response.json().then((data) => {
          this.$router.push({name: 'electionoverview', params: { electionId: data.id }})
        })
      }).catch(e => {
        this.$toasted.error(e.body.message)
      })
    }
  },
  created () {
    this.unsub = this.$store.subscribe((mutation, state) => console.log(mutation))
  },
  beforeDestroy () {
    console.log('before destroy')
    this.unsub()
  }
}
</script>
