<template>
    <v-container>
        <h3 class="my-3">Printing Authority</h3>

        <br>
        <div v-if="data.status == 0">
            Before voting sheets can be printed, the election administrator must set up the election.
        </div>

        <div v-if="data.status == 1">
            <v-btn color="primary" v-on:click="generateVotingSheets">Generate voting sheets</v-btn>
        </div>

        <div v-if="data.status == 2">
            todo: printing voting sheets
        </div>
    </v-container>
</template>

<script>
    export default {
        computed: {
            data() {
                return {
                    voters: this.$dataStore.state.election.voters,
                    status: this.$dataStore.state.election.status
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

            generateVotingSheets: function (event) {
                this.$socket.emit('generateVotingSheets', {'election': this.$route.params["id"]});
            }
        }
    };
</script>
