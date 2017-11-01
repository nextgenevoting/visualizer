<template>
    <v-container grid-list-md>
        <div v-if="this.$store.state.loaded">
            <ContentTitle icon="mdi-account-key" title="Election Administration"></ContentTitle>

            <div v-if="status == 0">
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

                    <v-btn color="primary" v-on:click="setUpElection" :disabled="!valid">setUpElection</v-btn>
                    <v-btn @click="clear">clear</v-btn>
                </v-form>
            </div>

            <div v-if="status == 1 || status == 2">
                The electorate data has been submitted to the printing authority.
            </div>

            <div v-if="status == 3">
                <v-btn>Decrypt & Tally</v-btn>
            </div>
        </div>
        <div v-else>
            <LoadingOverlay></LoadingOverlay>
        </div>
    </v-container>
</template>

<script>
    import { mapState } from 'vuex'
    import { mapGetters } from 'vuex'
    import joinRoomMixin from '../../mixins/joinRoomMixin.js'

    export default {
        mixins: [joinRoomMixin],
        data: () => ({
            valid: true,
            candidates: '["Yes", "No", "Maybe"]',
            numberOfVoters: '5',
            numberOfSelections: '[1]',
            numberOfCandidates: '[3]',
            countingCircles: '[1,1,1,1,1]'
        }),
        computed: {
            ...mapGetters({
                electionId: "electionId",
                status: "status",
            }),
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
                            if (data.result == 'success') {
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
            clear() {
                this.$refs.form.reset()
            }
        }
    };
</script>
