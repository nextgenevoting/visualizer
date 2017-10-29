<template>
    <v-container grid-list-md>
        <div class="layout row wrap">
            <div class="contentHeader">
                <i class="mdi icon mdi-account-key"></i>
            </div>
            <h3 class="my-3">Election Administration</h3>
        </div>

        <div v-if="data.status == 0">
            <v-form v-model="valid" ref="form" lazy-validation>
                <v-text-field
                        label="Candidates"
                        v-model="candidates"
                        required
                ></v-text-field>
                <v-text-field
                        label="Number of voters"
                        v-model="numberOfVoters"
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

        <div v-if="data.status == 1 || data.status == 2">
           The electorate data has been submitted to the printing authority.
        </div>

        <div v-if="data.status == 3">
            <v-btn>Decrypt & Tally</v-btn>
        </div>
    </v-container>
</template>

<script>
    export default {
        data: () => ({
            valid: true,
            candidates: '["Yes", "No", "Maybe"]',
            numberOfVoters: '5',
            numberOfSelections: '[1]',
            numberOfCandidates: '[3]',
            countingCircles: '[1,1,1,1,1]'
        }),
        computed: {
            data() {
                return {
                    voters: this.$store.state.BulletinBoard.voters,
                    candidates: this.$store.state.BulletinBoard.candidates,
                    publicVotingCredentials: this.$store.state.BulletinBoard.publicVotingCredentials,
                    numberOfSelections: this.$store.state.BulletinBoard.numberOfSelections,
                    status: this.$store.state.Election.status

                }
            }
        },
        created() {
            this.$socket.emit('join', {'election': this.$route.params["id"]});
        },
        methods: {

            setUpElection: function (event) {
                var self = this;
                if (this.$refs.form.validate()) {

                    //this.$socket.emit('setUpElection', {'election': this.$route.params["id"]});
                    this.$http.post('setUpElection',
                        {
                            'election': this.$route.params["id"],
                            'numberOfVoters': this.numberOfVoters,
                            'candidates': this.candidates,
                            'numberOfCandidates': this.numberOfCandidates,
                            'numberOfSelections': this.numberOfSelections,
                            'countingCircles': this.countingCircles,
                        }
                        ).then(response => {
                        response.json().then((data) => {
                            // success callback
                            if(data.result == 'success') {
                                this.$toasted.success("Successfully set up election");
                            }
                            else {
                                this.$toasted.error(data.message);
                            }

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
