<template>
    <v-container grid-list-md>
        <div v-if="this.$store.state.loaded">
            <ContentTitle icon="mdi-account" :title="selectedVoterName || 'Voter View'"></ContentTitle>
            <!--<v-btn flat color="blue" v-if="this.$store.state.selectedVoter != null" @click="changeVoter()" class="changeVoterButton">Change Voter</v-btn>-->
            <div v-if="status < 1">
                Before you can vote, the election must be set up
            </div>
            <div v-else>
                <v-flex xy12 md6 v-if="selectedVoter == null">Please choose a voter first<br>
                    <v-btn flat color="blue" @click="changeVoter">Select voter</v-btn>
                </v-flex>
                <v-flex xy12 md12 v-else>
                    <v-stepper color="blue" alt-labels :value="voter.status + 1">
                        <v-stepper-header>
                            <v-stepper-step step="1" :complete="voter.status >= 1">Vote Casting</v-stepper-step>
                            <v-divider></v-divider>
                            <v-stepper-step step="2" :complete="voter.status >= 2">Confirmation</v-stepper-step>
                            <v-divider></v-divider>
                            <v-stepper-step step="3" :complete="voter.status >= 3">Finalization</v-stepper-step>
                        </v-stepper-header>
                    </v-stepper>
                    <div class="layout row wrap">
                        <!-- 1. Vote Cast -->
                        <v-flex v-if="voter.status == 0" x12 md6>
                            <v-card v-if="hasVoterBallot > -1">
                                <v-card-title primary-title>
                                    <div class="headline">Waiting for authority response</div>
                                </v-card-title>
                                <v-card-text>
                                    Authority {{ hasVoterBallot + 1 }} is checking the ballot
                                    <v-progress-linear v-bind:indeterminate="true"></v-progress-linear>
                                </v-card-text>
                            </v-card>
                            <v-card v-else>
                                <v-card-title primary-title>
                                    <div class="headline">Vote Casting</div>
                                </v-card-title>
                                <v-card-text>
                                    <v-form ref="form" class="votingForm" lazy-validation>

                                    <ul v-for="(i,index) in numberOfParallelElections" class="electionForm">
                                        Your selection for election {{index + 1}}
                                        <li v-for="candidate in candidatesForElection[index]">
                                            <v-checkbox :label="candidate.name"
                                                        v-model="selection"
                                                        :value="candidate.index"
                                                        color="blue"
                                                        hide-details></v-checkbox>
                                        </li>
                                    </ul>
                                        <v-text-field label="Voting Code" v-model="votingCode" required></v-text-field>
                                    </v-form>

                                </v-card-text>
                                <v-card-actions>
                                    <v-btn flat color="blue" @click="castVote()">Cast vote</v-btn><v-btn flat>Abort</v-btn>
                                </v-card-actions>
                            </v-card>

                        </v-flex>
                        <!-- 2. Vote Confirmation -->
                        <v-flex v-if="voter.status == 1" x12 md6>
                            <v-card>
                                <v-card-title primary-title>
                                    <div class="headline">Vote Confirmation</div>
                                </v-card-title>
                                <v-card-text>
                                    <v-form ref="form" class="confirmationForm" lazy-validation>
                                        <p>Please check if the displayed codes match the verification codes of the selected candidates on your voting card:<br><br></p>
                                        <div>
                                        <ul>
                                            <li v-for="(verificationCode, index) in voter.verificationCodes">
                                                Verification Code {{index + 1}}: <b>{{ verificationCode }}</b>
                                            </li>
                                        </ul><br></div>
                                        <p>Please confirm your vote with your confirmation code:</p>
                                        <v-text-field label="Confirmation Code" v-model="confirmationCode" required></v-text-field>
                                    </v-form>

                                </v-card-text>
                                <v-card-actions>
                                    <v-btn flat color="blue" @click="castVote()">Confirm vote</v-btn><v-btn flat>Abort</v-btn>
                                </v-card-actions>
                            </v-card>

                        </v-flex>
                        <!-- 3. Vote Finalization -->

                        <v-flex x12 md6>{{ votingCard }}</v-flex>
                    </div>
                    <v-tooltip left>
                        <v-btn slot="activator"  color="blue" fab fixed top right dark style="top: 150px;"  v-if="this.$store.state.selectedVoter != null" @click="changeVoter()"><v-icon>mdi-account-multiple</v-icon></v-btn>
                        <span>Change voter</span>
                    </v-tooltip>
                </v-flex>
            </div>
        </div>
        <div v-else>
            <LoadingOverlay></LoadingOverlay>
        </div>
        <SelectVoterDialog></SelectVoterDialog>
    </v-container>
</template>

<script>
    import { mapState } from 'vuex'
    import { mapGetters } from 'vuex'
    import joinRoomMixin from '../../mixins/joinRoomMixin.js'

    export default {
        mixins: [joinRoomMixin],
        data: () => ({
            selection: [],
            votingCode: '',
            confirmationCode: ''

        }),
        computed: {
            ...mapState({
                selectedVoter: state => state.selectedVoter,
                numberOfParallelElections: state => state.BulletinBoard.numberOfParallelElections,
                candidates: state => state.BulletinBoard.candidates,
                numberOfCandidates: state => state.BulletinBoard.numberOfCandidates,
                publicKey: state => state.BulletinBoard.publicKey
            }),
            ...mapGetters({
                electionId: "electionId",
                status: "status",
            }),

            voter: {
                get: function () {
                    return this.$store.getters.getVoter(this.selectedVoter);
                }
            },
            votingCard: {
                get: function () {
                    if (this.selectedVoter != null) {
                        return this.$store.getters.getVotingCard(this.selectedVoter);
                    }
                }
            },
            selectedVoterName: {
                get() {
                    if (this.$store.state.selectedVoter != null) {
                        return this.$store.getters.getVoter(this.$store.state.selectedVoter).name;
                    } else {
                        return '';
                    }
                }
            },
            candidatesForElection: {
                get: function () {
                    var candidatesForElections = [];
                    for (var j = 0; j < this.numberOfParallelElections; j++) {
                        var startIndex = 0;
                        var candidates = [];

                        for (var i = 0; i < j; i++) {
                            startIndex += this.numberOfCandidates[i];
                        }
                        for (var i = 0; i < this.numberOfCandidates[j]; i++) {
                            candidates.push({
                                name: this.candidates[startIndex + i],
                                index: startIndex + i,
                                checked: false
                            });
                        }
                        candidatesForElections.push(candidates);
                    }
                    return candidatesForElections;
                }
            },
            hasVoterBallot: {
                get: function(){
                    return this.$store.getters.hasVoterBallot(this.$store.state.selectedVoter);
                }
            }
        },
        methods: {
            generateVotingSheets: function (event) {
                this.$socket.emit('generateVotingSheets', {'election': this.$route.params["id"]});
            },
            changeVoter: function () {
                this.$store.commit("voterDialog", true);
            },
            castVote: function () {
                var selection = this.selection.sort();
                var voterId = this.selectedVoter;
                this.$http.post('castVote',
                    {
                        'election': this.$route.params["id"],
                        'selection': this.selection.sort(),
                        'voterId': this.selectedVoter,
                        'votingCode': this.votingCode
                    }
                ).then(response => {
                    response.json().then((data) => {
                        // success callback
                        if (data.result == 'success')
                            this.$toasted.success("Successfully cast vote");
                        else
                            this.$toasted.error(data.message);

                    });
                }, response => {
                    // error callback
                });
            }
        },
        watch: {
            selectedVoter: function (newValue) {
                console.log('voter changed');
                this.selection = [];
                this.votingCode = "";
            }
        },
    };
</script>
<style>
    .application--light .stepper {
        background: transparent !important;
    }

    .stepper {
        box-shadow: none !important;
        margin-top: -20px;
    }
    .application--light .stepper .stepper__step__step{
        box-shadow: 0 0 2px 2px rgba(0,0,0,.2), 0px 0px 0px 0px rgba(0,0,0,.14), 0 1px 10px rgba(0,0,0,.12);

    }

    .stepper__step--active .stepper__step__step, .stepper__step--complete .stepper__step__step {
        background: #696969 ;
    }
    .application--light .stepper .stepper__step:not(.stepper__step--active):not(.stepper__step--complete):not(.stepper__step--error) .stepper__step__step {
        background: rgba(0, 0, 0, 0.2) !important;
    }

    .electionForm{
        width:100%;
        margin-bottom: 20px;
    }

</style>