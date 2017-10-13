<template>
    <v-container>
        <h3 class="my-3">Election overview</h3>
        <br>
        Count: <b>{{ data.count }}</b>
        <br>
        <v-btn color="primary" v-on:click="increment">Increment</v-btn>
        <br>


    </v-container>
</template>

<script>
    export default {
        computed: {
            data() {
                return {
                    count: this.$dataStore.state.election.count

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

            increment: function (event) {
                this.$socket.emit('increment', {'election': this.$route.params["id"]});
                //console.log("Increment called");
                //this.$dataStore.dispatch('increment')
            }
        }
    };
</script>
