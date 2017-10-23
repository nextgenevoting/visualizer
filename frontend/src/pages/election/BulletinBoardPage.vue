<template>
    <v-container>
        <h3 class="my-3">Bulletin Board</h3>
        Unique election identifier: <b>{{ data.id }}</b>
        <br>
        Status: <b>{{ data.status }}</b>
        <br>
        Public Key: <BigIntLabel :mpzValue="data.publicKey"></BigIntLabel>
        <br>
        Voters: <b>{{ data.voters }}</b><br>
        Candidates: <b>{{ data.candidates }}</b><br>
        Number of selections: <b>{{ data.numberOfSelections }}</b><br>
        Public voting credentials: <b>{{ data.publicVotingCredentials }}</b><br>
        Counting circles: <b>{{ data.countingCircles }}</b><br>

        <br>
    </v-container>
</template>

<script>
    export default {
        computed: {
            data() {
                return {
                    id: this.$store.state.BulletinBoard.id,
                    status: this.$store.getters.getStatusText,
                    publicKey: this.$store.state.BulletinBoard.publicKey,
                    voters: this.$store.state.BulletinBoard.voters,
                    candidates: this.$store.state.BulletinBoard.candidates,
                    publicVotingCredentials: this.$store.state.BulletinBoard.publicVotingCredentials,
                    numberOfSelections: this.$store.state.BulletinBoard.numberOfSelections,
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
        }
    };
</script>
