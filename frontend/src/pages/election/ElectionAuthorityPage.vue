<template>
    <v-container grid-list-md>
        <div v-if="this.$store.state.loaded">
            <ContentTitle icon="mdi-settings-box" title="Election Authorities"></ContentTitle>

            <v-flex xs12 sm12>
                <v-btn-toggle v-model="currentAuthority">
                    <v-btn flat>
                        Authority 1
                    </v-btn>
                    <v-btn flat>
                        Authority 2
                    </v-btn>
                    <v-btn flat>
                        Authority 3
                    </v-btn>

                </v-btn-toggle>
            </v-flex>

            <br>
            <h5 class="">Tasks</h5>
            <v-layout row v-for="voterBallot in voterBallots">
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
            </v-layout>

            <br>
            <br>
            <h5 class="">Data</h5>

            <v-layout row wrap>

                <v-flex xy12 md12>
                    <DataCard title="Ballots" :isMpz=true :expandable=false confidentiality="encrypted">
                        <transition-group tag="ul" name="highlight" :appear="ballotTransition">
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
        }),
        mounted() {
            this.ballotTransition = false
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
                    // bug: if the page if reloaded, it tries to access electionAuthority[0] even though they haven't been populated by the websocket sync yet
                    return this.$store.getters.getElectionAuthority(this.currentAuthority+1);
                }
            },
            voterBallots: {
                get: function () {
                    return this.$store.getters.getVoterBallots(this.currentAuthority+1);
                }
            },
            ballots: {
                get: function () {
                    return this.$store.getters.getBallots(this.currentAuthority+1);
                }
            },

        },
        methods: {
            checkBallot: function (voterId) {
                this.$http.post('checkVote',
                    {
                        'election': this.$route.params["id"],
                        'authorityId': this.currentAuthority+1,
                        'voterId': voterId,
                    }
                ).then(response => {
                    response.json().then((data) => {
                        // success callback
                        if (data.result == 'success')
                            this.$toasted.success("Successfully checked vote");
                        else
                            this.$toasted.error(data.message);

                    });
                }, response => {
                    // error callback
                });
            }
        },

    };
</script>

<style>
    .btn-toggle {
        width: 100%;
    }

    .btn-toggle .btn {
        width: 33%;
    }

    .highlight-enter-active {
        animation: highlight 2.5s;
    }
    @keyframes highlight {
        0% {
            background: inherit;
        }
        50% {
            background: yellow;
        }
        100% {
            background: inherit;
        }
    }
</style>