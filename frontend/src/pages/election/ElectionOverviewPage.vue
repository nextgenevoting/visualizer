<template>
    <v-container>
        <h3 class="my-3">Election overview</h3>
        ID: <b>{{ data.id }}</b>
        <br>
        Status: <b>{{ data.status }}</b>
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
                    status: this.$store.getters.getStatusText
                }
            },
        },
        created(){
            this.$socket.emit('join', {'election': this.$route.params["id"]});
        }
    };
</script>
