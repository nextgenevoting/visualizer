<template>
    <v-container>
        <h3 class="my-3">Election Administration</h3>


        <div>
            <v-form v-model="valid" ref="form" lazy-validation>
                <v-text-field
                        label="Candidates"
                        v-model="candidates"
                        required
                ></v-text-field>
                <v-text-field
                        label="Voters"
                        v-model="voters"
                        required
                ></v-text-field>
                <v-text-field
                        label="Number of Candidates"
                        v-model="numberOfCandidates"
                        required
                ></v-text-field>
                <v-text-field
                        label="Number of selections"
                        v-model="numberOfSelections"
                        required
                ></v-text-field>
                <v-text-field
                        label="Counting Circles"
                        v-model="countingCircles"
                        required
                ></v-text-field>

                <v-btn color="primary" v-on:click="setUpElection":disabled="!valid">setUpElection</v-btn>
                <v-btn @click="clear">clear</v-btn>
            </v-form>
        </div>

        <div v-if="data.status > 0">
            Voters: <b>{{ data.voters }}</b><br>
            Candidates: <b>{{ data.candidates }}</b><br>
            Number of selections: <b>{{ data.numberOfSelections }}</b><br>
            Public voting credentials: <b>{{ data.publicVotingCredentials }}</b><br>
            Counting circles: <b>{{ data.countingCircles }}</b><br>

            <br>
        </div>
    </v-container>
</template>

<script>
    export default {
        data: () => ({
            valid: true,
            candidates: '["Clinton", "Trump"]',
            voters: '["Voter1", "Voter 2"]',
            numberOfSelections: '[1]',
            numberOfCandidates: '[1]',
            countingCircles: '[1, 1]'
        }),
        computed: {
            data() {
                return {
                    voters: this.$dataStore.state.election.voters,
                    candidates: this.$dataStore.state.election.candidates,
                    publicVotingCredentials: this.$dataStore.state.election.publicVotingCredentials,
                    numberOfSelections: this.$dataStore.state.election.numberOfSelections,
                    status: this.$dataStore.state.election.status

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

            setUpElection: function (event) {
                if (this.$refs.form.validate()) {

                    //this.$socket.emit('setUpElection', {'election': this.$route.params["id"]});
                    this.$http.post('setUpElection',
                        {
                            'election': this.$route.params["id"],
                            'voters': this.voters,
                            'candidates': this.candidates,
                            'numberOfCandidates': this.numberOfCandidates,
                            'numberOfSelections': this.numberOfSelections,
                            'countingCircles': this.countingCircles,
                        }
                        ).then(response => {
                        response.json().then((data) => {
                            // success callback
                        });
                    }, response => {
                        // error callback
                    });
                }
            },
            clear () {
                this.$refs.form.reset()
            }
        }
    };
</script>
