<template>
    <v-container>
        <h3 class="my-3">Bulletin Board</h3>
        Unique election identifier: <b>{{ data.id }}</b>
        <br>
        Status: <b>{{ data.status }}</b>
        <br>
        Public Key: <b>{{ data.publicKey }}</b>

        <br>
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
                    publicKey: this.$store.state.BulletinBoard.publicKey
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
    };
</script>
