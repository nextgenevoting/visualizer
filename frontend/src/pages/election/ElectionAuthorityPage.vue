<template>
    <v-container>
        <h3 class="my-3">Election Authority</h3>


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
};
</script>
