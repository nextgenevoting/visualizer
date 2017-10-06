<template>
 <v-container grid-list-xl text-xs-center>
    <v-layout row wrap>
      <v-flex xs10 offset-xs1>
        <v-card class="pa-5">
           <span class="headline">Login</span>
           <v-form v-model="valid">
              <v-text-field
                label="Name"
                v-model="name"
                :rules="nameRules"
                :counter="10"
                required
              ></v-text-field>
              <v-text-field
                label="Password"
                v-model="email"
                :rules="emailRules"
                required
              ></v-text-field>
              <v-btn @click="clear" class="">Login</v-btn>
            </v-form>
        </v-card>
      </v-flex>
    </v-layout>
 </v-container>
</template>

  <script>
  export default {
    data() {
      return {
        // We need to initialize the component with any
        // properties that will be used in it
        credentials: {
          username: '',
          password: ''
        },
        error: ''
      }
    },
    methods: {
      submit() {
        var credentials = {
          username: this.credentials.username,
          password: this.credentials.password
        }
        // We need to pass the component's this context
        // to properly make use of http in the auth service
        // auth.login(this, credentials, 'secretquote')
      }
    }

  }
  </script>