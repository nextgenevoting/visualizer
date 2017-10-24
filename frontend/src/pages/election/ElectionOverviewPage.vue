<template>
    <v-container>
        <h3 class="my-3">Election overview</h3>
        ID: <b>{{ data.id }}</b>
        <br>
        Status: <b>{{ data.status }}</b>
        <br>
        <br>
        <v-btn color="primary" v-on:click="debugVotingSim">Debug VoteSim trigger</v-btn>
    </v-container>
</template>

<script>
export default {
  computed: {
    data() {
      return {
        id: this.$store.state.Election.electionID,
        status: this.$store.getters.getStatusText,
      };
    },
  },
  created() {
    this.$socket.emit('join', {election: this.$route.params['id'] });
  },
  methods: {
      debugVotingSim: function (event) {
          this.$http.post('debugVotingSim', {
                  'election': this.$route.params["id"],
              }
          ).then(response => {
              response.json().then((data) => {
                  // success callback
              });
          }, response => {
              // error callback
          });
      },
  }
};
</script>
