<template>
    <v-container grid-list-md>
        <div v-if="this.$store.state.loaded">
            <ContentTitle icon="mdi-settings-box" title="Election Authorities"></ContentTitle>

            <v-flex xs12 sm12>
                <v-btn-toggle v-model="currentAuthority">
                    <v-btn flat v-for="auth in electionAuthorities">
                        <v-badge color="blue" right>
                            <span slot="badge" v-if="auth.voterBallots.length > 0">{{ auth.voterBallots.length }}</span>
                            <v-icon>mdi-settings-box</v-icon> Election Authority {{auth.id + 1}}
                        </v-badge>
                    </v-btn>
                </v-btn-toggle>
            </v-flex>

            <br>
            <h5 class="">Tasks</h5>
            <transition-group tag="div" :name="checkTransitionClass" :appear="checkTransition">
                <v-layout row v-for="voterBallot in voterBallots" :key="voterBallot.voterId">
                    <v-flex xs12 sm12 >
                        <v-card>
                            <v-card-title primary-title>
                                <div>
                                    <div class="headline">New ballot submitted</div>
                                </div>
                            </v-card-title>
                            <v-card-text>
                                <p>Please check the ballot and respond to the query</p>
                            </v-card-text>
                            <v-card-text v-if="voterBallot.checkResults[currentAuthority] != null">
                            Result of Check: {{ voterBallot.checkResults[currentAuthority] }}
                            </v-card-text>
                            <v-card-actions>
                                <v-btn flat color="blue" @click="checkBallot(voterBallot.voterId)"><v-icon left>mdi-approval</v-icon> Check Validity</v-btn>
                                <v-btn flat color="blue" @click="respond(voterBallot.voterId)" :disabled="!voterBallot.checkResults[currentAuthority]"><v-icon left>mdi-reply</v-icon>Respond to query</v-btn>
                                <v-btn flat color="red" @click="discardBallot(voterBallot.voterId)" :disabled="voterBallot.checkResults[currentAuthority] || voterBallot.checkResults[currentAuthority] == null"><v-icon left>mdi-cancel</v-icon>Discard ballot</v-btn>
                                <v-spacer></v-spacer>
                                <v-btn icon @click.native="show = !show">
                                    <v-icon>{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
                                </v-btn>
                            </v-card-actions>
                            <v-slide-y-transition>
                                <v-card-text v-show="show">
                                    a_bold: {{ voterBallot.ballot.a_bold }}<br>
                                    x_hat: {{ voterBallot.ballot.x_hat }}
                                </v-card-text>
                            </v-slide-y-transition>
                        </v-card>
                    </v-flex>
                </v-layout>
            </transition-group>


            <!--<v-layout row v-for="voterBallot in voterBallots">
                <v-flex xs12 sm12 >
                    <v-card>
                        <v-card-title primary-title>
                            <div>
                                <div class="headline">New ballot submitted</div>
                            </div>
                        </v-card-title>
                        <v-card-text>
                            <p>Please check the ballot and respond to the query</p>
                        </v-card-text>
                        <v-card-actions>
                            <v-btn flat color="blue" @click="checkBallot(voterBallot.voterId)">Check & Respond</v-btn>
                            <v-spacer></v-spacer>
                            <v-btn icon @click.native="show = !show">
                                <v-icon>{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
                            </v-btn>
                        </v-card-actions>
                        <v-slide-y-transition>
                            <v-card-text v-show="show">
                                a_bold: {{ voterBallot.ballot.a_bold }}<br>
                                x_hat: {{ voterBallot.ballot.x_hat }}
                            </v-card-text>
                        </v-slide-y-transition>
                    </v-card>
                </v-flex>
            </v-layout>-->

            <br>
            <br>
            <h5 class="">Data</h5>

            <v-layout row wrap>

                <v-flex xy12 md12>
                    <DataCard title="Ballots" :isMpz=true :expandable=false confidentiality="encrypted">
                        <transition-group tag="ul" :name="ballotTransitionClass" :appear="ballotTransition">
                            <li v-for="ballot in ballots" :key="ballot.ballot.x_hat">Ballot: {{ballot.ballot.a_bold}}</li>
                        </transition-group>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Public Key" :isMpz=true :expandable=false confidentiality="public">
                        <BigIntLabel :mpzValue="electionAuthority.publicKey"></BigIntLabel>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Public Key Share" :isMpz=true :expandable=false confidentiality="public">
                        <BigIntLabel :mpzValue="electionAuthority.publicKeyShare"></BigIntLabel>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Secret Key Share" :isMpz=true :expandable=false confidentiality="secret">
                        <BigIntLabel :mpzValue="electionAuthority.secretKeyShare"></BigIntLabel>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4 v-if="expertMode">
                    <DataCard title="Points" :expandable=true confidentiality="secret">
                        Points of all voters
                        <ul id="subList" slot="expandContent">
                            <li v-for="(voter, index) in electionAuthority.points">
                                Voter {{ index}}
                                <ul id="subList">
                                    <li v-for="point in voter">
                                        x:
                                        <BigIntLabel :mpzValue="point[0]"></BigIntLabel>
                                        y:
                                        <BigIntLabel :mpzValue="point[1]"></BigIntLabel>
                                    </li>
                                </ul>

                            </li>
                        </ul>
                    </DataCard>
                </v-flex>
            </v-layout>
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
            currentAuthority: 0,
            show: false,
            ballotTransition: false,
            checkTransition: false,
            ballotTransitionClass: 'highlight',
            checkTransitionClass: 'bounce'
        }),
        mounted() {
            this.ballotTransition = false
            this.checkTransition = false
        },
        computed: {
            ...mapState({
                electionAuthorities: state => state.ElectionAuthority.electionAuthorities,
                expertMode: state => state.BulletinBoard.expertMode
            }),
            ...mapGetters({
                electionId: "electionId",
            }),
            electionAuthority: {
                get: function () {
                    return this.$store.getters.getElectionAuthority(this.currentAuthority);
                }
            },
            voterBallots: {
                get: function () {
                    return this.$store.getters.getVoterBallots(this.currentAuthority);
                }
            },
            ballots: {
                get: function () {
                    return this.$store.getters.getBallots(this.currentAuthority);
                }
            },

        },
        methods: {
            checkBallot: function (voterId) {
                this.$http.post('checkVote', {
                    'election': this.$route.params["id"],
                    'authorityId': this.currentAuthority,
                    'voterId': voterId,
                }).then(response => {
                    response.json().then((data) => {
                        // success callback
                        this.$toasted.success("Successfully checked vote");
                    });
                }).catch(e => {
                    this.$toasted.error(e.body.message);
                })
            },
            respond: function (voterId) {
                this.$http.post('respond', {
                    'election': this.$route.params["id"],
                    'authorityId': this.currentAuthority,
                    'voterId': voterId,
                }).then(response => {
                    response.json().then((data) => {
                        // success callback
                        this.$toasted.success("Successfully replied to vote");
                    });
                }).catch(e => {
                    this.$toasted.error(e.body.message);
                })
            },
            discardBallot: function (voterId) {
                this.$http.post('discardBallot', {
                    'election': this.$route.params["id"],
                    'authorityId': this.currentAuthority,
                    'voterId': voterId,
                }).then(response => {
                    response.json().then((data) => {
                        // success callback
                        this.$toasted.success("Successfully replied to vote");
                    });
                }).catch(e => {
                    this.$toasted.error(e.body.message);
                })
            },
        },
        watch: {
            currentAuthority: function (newAuthority) {
                // Transition animation is also shown when the selected authority has changed. As a workaround, temporarily remove the CSS transition class and re-assign it after some delay
                let self = this;
                let savedTransitionClass = this.ballotTransitionClass;
                let savedCheckTransitionClass = this.checkTransitionClass;
                this.ballotTransitionClass = "";
                this.checkTransitionClass = "";
                setTimeout(function(){
                    self.ballotTransitionClass = savedTransitionClass;
                    self.checkTransitionClass = savedCheckTransitionClass
                }, 1000);
            }
        },

    };
</script>

<style>
    .btn-toggle {
        width: 100%;
        background-color: transparent !important;
    }

    .btn-toggle .btn {
        width: 33%;
    }
    .btn-toggle--selected {
        box-shadow: none;
    }
    .btn-toggle .icon{
        display: none;
    }

    .btn--active .icon{
        display: inline-flex;
    }

    .highlight-enter-active {
        animation: highlight 2.0s;
    }
    @keyframes highlight {
        0% {
            background: inherit;
        }
        50% {
            background: rgba(11, 176, 255, 0.4);
        }
        100% {
            background: inherit;
        }
    }

    .bounce-enter-active {
        animation: bounce-in .5s;
    }
    .bounce-leave-active {
        animation: bounce-in .4s reverse;
    }
    @keyframes bounce-in {
        0% {
            transform: scale(0);
            opacity: 0;
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }
</style>