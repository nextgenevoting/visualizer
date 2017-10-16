<template>
    <v-container>
        <h3 class="my-3">Election Administration</h3>
        Voters: <b>{{ data.voters }}</b><br>
        Candidates: <b>{{ data.candidates }}</b><br>
        Number of selections: <b>{{ data.numberOfSelections }}</b><br>
        Public voting credentials: <b>{{ data.publicVotingCredentials }}</b><br>
        <br>
        <v-btn color="primary" v-on:click="setUpElection">setUpElection</v-btn>

    </v-container>
</template>

<script>
    export default {
        computed: {
            data() {
                return {
                    voters: this.$dataStore.state.election.voters,
                    candidates: this.$dataStore.state.election.candidates,
                    publicVotingCredentials: this.$dataStore.state.election.publicVotingCredentials,
                    numberOfSelections: this.$dataStore.state.election.numberOfSelections

                }
            }
        },
        created() {
            this.$socket.emit('join', {'election': this.$route.params["id"]});
            this.unsub = this.$dataStore.subscribe((mutation, state) => console.log(mutation));
        },
        beforeDestroy() {
            console.log("before destroy");
            this.unsub();
        },
        methods: {

            setUpElection: function (event) {
                this.$socket.emit('setUpElection', {'election': this.$route.params["id"]});
                //console.log("Increment called");
                //this.$dataStore.dispatch('increment')
            }
        }
    };
</script>
