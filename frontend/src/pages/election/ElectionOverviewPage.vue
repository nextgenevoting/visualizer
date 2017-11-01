<template>
    <v-container>
        <div v-if="this.$store.state.loaded">
            <ContentTitle icon="mdi-view-dashboard" title="Overview"></ContentTitle>

            ID: <b>{{ id }}</b>
            <br>
            Status: <b>{{ status }}</b>
            <br>
            <br>
            <v-btn color="primary" v-on:click="debugVotingSim">Debug VoteSim trigger</v-btn>
        </div>
        <div v-else>
            <LoadingOverlay></LoadingOverlay>
        </div>
    </v-container>
</template>

<script>
    export default {
        computed: {
            id: {
                get: function () {
                    return this.$store.getters.electionId;
                }
            },
            status: {
                get: function () {
                    return this.$store.getters.statusText;
                }
            },
        },
        created() {
            if (this.$store.getters.joinedElectionId !== this.$route.params['id'])
                this.$socket.emit('join', {election: this.$route.params['id']});
        },
        methods: {
            debugVotingSim: function (event) {
                this.$http.post('debugVotingSim', {
                    'election': this.$route.params['id']
                }).then(response => {
                    response.json().then((data) => {
                        // success callback
                    })
                }, response => {
                    // error callback
                })
            }
        },
        watch: {
            // whenever question changes, this function will run
            status: function (newStatus) {
                console.log("Status Watcher:" + newStatus);
            }
        },
    }
</script>