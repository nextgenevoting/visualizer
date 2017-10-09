<template>
    <v-container>
        <h3 class="my-3">Election overview</h3>
        Websocket Connection: <b>{{ data.connected.toString() }}</b>
        <br>
        Count: <b>{{ data.count }}</b>
        <br>
        <v-btn color="primary" v-on:click="increment">Increment</v-btn>
        <br>
        Voters: <b>{{ data.voters }}</b><br>
        Candidates: <b>{{ data.candidates }}</b>
        <br>
        <v-btn color="primary" v-on:click="setUpElection">setUpElection</v-btn>

    </v-container>
</template>

<script>
    export default {
        computed: {
            data() {
                return {
                    count: this.$dataStore.state.election.count,
                    voters: this.$dataStore.state.election.voters,
                    candidates: this.$dataStore.state.election.candidates,
                    connected: this.$dataStore.state.connected
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

            increment: function (event) {
                this.$socket.emit('increment', {'election': this.$route.params["id"]});
                //console.log("Increment called");
                //this.$dataStore.dispatch('increment')
            },
            setUpElection: function (event) {
                this.$socket.emit('setUpElection', {'election': this.$route.params["id"]});
                //console.log("Increment called");
                //this.$dataStore.dispatch('increment')
            }
        }
    };
</script>
