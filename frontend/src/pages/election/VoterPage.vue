<template>
    <v-container>
        <h3 class="my-3">Voter</h3>

        <br>
        <div v-if="data.status < 3">
            Before you can vote, the election must be set up and voting cards printed
        </div>
        <div v-if="data.status == 3">
            todo: Vote casting
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
