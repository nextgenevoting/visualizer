<template>
    <v-container>
        <div class="layout row wrap">
            <div class="contentHeader">
                <i class="mdi icon mdi-account"></i>
            </div>
            <h3 class="my-3">Voter</h3>
        </div>
        <br>
        <div v-if="data.status < 3">
            Before you can vote, the election must be set up and voting cards printed
        </div>
        <div v-if="data.status == 3">
            todo: Vote casting<br><br>
            {{ data.votingCards }}

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
                    votingCards: this.$store.state.Voter.voters,
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

            generateVotingSheets: function (event) {
                this.$socket.emit('generateVotingSheets', {'election': this.$route.params["id"]});
            }
        }
    };
</script>
