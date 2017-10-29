<template>
  <v-container grid-list-xl text-xs-center>
    <v-layout row wrap>
      <v-flex xs10 offset-xs1>
        <v-card class="pa-5">
          <span class="headline">Login</span>
          <v-form v-model="valid">
            <v-text-field label="Name" v-model="name" :rules="nameRules" :counter="10" required />
            <v-text-field label="Password" v-model="email" :rules="emailRules" required />
            <v-btn @click="submit" v-t="'login'" />
          </v-form>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<i18n>
en:
  login: Login
de:
  login: Anmelden
</i18n>

<script>
export default {
  data () {
    return {
      credentials: {
        username: '',
        password: ''
      },
      error: ''
    }
  },
  methods: {
    submit () { }
  }
}
</script>
