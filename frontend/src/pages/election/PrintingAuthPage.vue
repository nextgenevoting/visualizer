<template>
    <v-container>
        <h3 class="my-3">Printing Authority</h3>

        <br>
        <div v-if="data.status == 0">
            Before voting sheets can be printed, the election administrator must set up the election.
        </div>

        <div v-if="data.status == 1">
            <v-btn color="primary" v-on:click="printVotingCards">Print voting sheets</v-btn>
        </div>

        <div v-if="data.status == 2">
            todo: printing voting sheets<br><br>
            Voting Sheets: {{ data.votingCards }}

        </div>
    </v-container>
</template>

<script>
    export default {
        computed: {
            data() {
                return {
                    voters: this.$store.state.BulletinBoard.voters,
                    status: this.$store.state.Election.status,
                    votingCards: this.$store.state.PrintingAuthority.votingCards
                }
            }
        },
        created() {
            this.$socket.emit('join', {'election': this.$route.params["id"]});
            this.unsub = this.$store.subscribe((mutation, state) => console.log(mutation));
        },
        beforeDestroy() {
            console.log("before destroy");
            this.unsub();
        },
        methods: {

            printVotingCards: function (event) {
               this.$http.post('printVotingCards',
                   {
                       'election': this.$route.params["id"],
                   }
                   ).then(response => {
                   response.json().then((data) => {
                       // success callback
                   });
               }, response => {
                   // error callback
               });
            }
        }
    };
</script>
