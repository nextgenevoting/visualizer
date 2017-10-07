<template>
    <v-container>
        <h3 class="my-3">Election overview</h3>
        Websocket Connection: <b>{{ data.connected.toString() }}</b>
        <br>
        Message: <b>{{ data.message }}</b>
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
                    message: this.$dataStore.state.elections.message,
                    connected: this.$dataStore.state.connected

                }
            }
        },
        mounted() {
            this.$dataStore.subscribe((mutation, state) => console.log(mutation));
        },
        methods: {

            increment: function (event) {
                this.$socket.emit('increment');
                //console.log("Increment called");
                //this.$dataStore.dispatch('increment')
            }
        }
    };
</script>
