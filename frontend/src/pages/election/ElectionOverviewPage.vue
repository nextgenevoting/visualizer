<template>
    <v-container>
        <div class="layout row wrap">
            <div class="contentHeader">
                <i class="mdi icon mdi-view-dashboard"></i>
            </div>
            <h3 class="my-3">Overview</h3>
        </div>

        ID: <b>{{ id }}</b>
        <br>
        Status: <b>{{ status }}</b>
        <br>
        <br>
        <v-btn color="primary" v-on:click="debugVotingSim">Debug VoteSim trigger</v-btn>
    </v-container>
</template>

<script>
    export default {
        computed: {
            id: {
                get: function(){
                    return this.$store.getters.electionId;
                }
            },
            status: {
                get: function(){
                    return this.$store.getters.statusText;
                }
            },
        },
        created () {
            if(this.$store.getters.joinedElectionId !== this.$route.params['id'])
                console.log("Join in overview!");
                this.$socket.emit('join', { election: this.$route.params['id'] });
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