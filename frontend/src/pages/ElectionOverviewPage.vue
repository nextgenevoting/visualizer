<template>
    <v-container>
        <h3 class="my-3">Election overview</h3>
        Websocket Connection: <b>{{ data.connected.toString() }}</b>
        <br>
        Count: <b>{{ data.count }}</b>
        <br>
        <v-btn color="primary" v-on:click="increment">Increment</v-btn>
    </v-container>
</template>

<script>
    export default {
        computed: {
            data() {
                return {
                    count: this.$dataStore.state.elections.count,
                    connected: this.$dataStore.state.connected
                }
            }
        },
        mounted() {
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
            }
        }
    };
</script>
