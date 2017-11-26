<template>
  <v-container grid-list-xl text-xs-center>
    <v-layout row wrap>
      <v-flex xs10 offset-xs1>
        <v-card class="pa-5">
          <span class="headline" v-t="'electionsPage.create'" />
          <v-form @submit.prevent="createElection">
            <v-text-field :label="$t('title')" v-model="title" required autofocus />
            <v-select
                    :items="this.securityLevels"
                    v-model="securityLevel"
                    item-value="id"
                    item-text="label"
                    label="Security Level"
                    single-line
                    bottom
            ></v-select>
            <v-btn type="submit" color="primary">{{ $t('create') }}</v-btn>
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
      title: '',
      securityLevel: 1,
      securityLevels: [{id: 1, label: 'Security Level 1 (1024 bit)'}, {id: 2, label: 'Security Level 2 (2048 bit)'}, {id: 3, label: 'Security Level 3 (3072 bit)'}]
    }
  },
  methods: {
    createElection () {
      this.$http.post('createElection', {title: this.title, securityLevel: this.securityLevel}).then(response => {
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
    this.unsub()
  }
}
</script>
