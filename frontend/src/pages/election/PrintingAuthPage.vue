<template>
    <v-container grid-list-md>
        <div class="layout row wrap">
            <div class="contentHeader">
                <i class="mdi icon mdi-printer"></i>
            </div>
            <h3 class="my-3">Printing Authority</h3>
        </div>
        <div>
            <h5 class="">Tasks</h5>
            <v-alert v-if="data.status == 3" color="grey lighten-3" icon="check_circle" value="true"
                     v-model="sentAlert">
                Voting cards have been delivered to the voters!
            </v-alert>
            <!-- <v-alert v-if="data.status == 3" color="info" icon="info" value="true" v-model="sentAlert">
                 Voting cards have been delivered to the voters!
             </v-alert>-->
            <p v-if="data.status == 0">
                Before voting cards can be printed, the election administrator must set up the election.</p>
            <div v-if="data.status < 3">
                <v-btn v-on:click="printVotingCards" :disabled="data.status != 1">
                    <v-icon>mdi-printer</v-icon>
                    Print voting cards
                </v-btn>
                <v-btn v-on:click="sendVotingCards" :disabled="data.status != 2">
                    <v-icon>mdi-email</v-icon>
                    Send voting cards to voters
                </v-btn>
            </div>
        </div>

        <h5 class="">Data</h5>

        <v-layout row wrap>

            <v-flex xy12 md12 v-if="data.status >=2">
                <DataCard title="Voting Cards" :expandable=false confidentiality="secret" :disableTooltip="true">
                    <v-layout row wrap>

                        <v-flex xy12 md2>

                            <v-list>
                                <v-list-tile v-for="(item, index) in data.voters" v-bind:key="item.name"
                                             active-class="default-class your-class"
                                             @click="selectedVoter = index-1">
                                    <v-list-tile-content>
                                        <v-list-tile-title>{{ item.name }}</v-list-tile-title>
                                    </v-list-tile-content>

                                </v-list-tile>
                            </v-list>

                        </v-flex>

                        <v-flex xy12 md10>
                            {{ data.getVotingCard() }}

                        </v-flex>
                    </v-layout>

                </DataCard>

            </v-flex>


            <v-flex xy12 md12 v-if="this.$store.state.expertMode">
                <DataCard title="Private Voter Data" :expandable=false confidentiality="secret">
                    {{data.privateCredentials}}
                </DataCard>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    export default {
        data: () => ({
            selectedVoter: 0,
            sentAlert: true
        }),
        computed: {
            data() {
                var self = this;
                return {
                    voters: this.$store.state.Voter.voters,
                    status: this.$store.state.Election.status,
                    privateCredentials: this.$store.state.PrintingAuthority.privateCredentials,
                    votingCards: this.$store.state.PrintingAuthority.votingCards,
                    getVotingCard: function () {
                        if (self.selectedVoter <= self.$store.state.PrintingAuthority.votingCards.length) {
                            return self.$store.state.PrintingAuthority.votingCards[self.selectedVoter];
                        } else {
                            return "";
                        }
                    }
                }
            }
        },
        created() {
            this.$socket.emit('join', {'election': this.$route.params["id"]});
        },
        methods: {
            printVotingCards: function (event) {
                this.$http.post('printVotingCards', {
                        'election': this.$route.params["id"],
                    }
                ).then(response => {
                    response.json().then((data) => {
                        // success callback
                        if (data.result == 'success') {
                            this.$toasted.success("Successfully printed voting sheets");
                            this.selectedVoter = 0;
                        }
                        else {
                            this.$toasted.error(data.message);
                        }
                    });
                }, response => {
                    // error callback
                });
            },
            sendVotingCards: function (event) {
                this.$http.post('sendVotingCards', {
                        'election': this.$route.params["id"],
                    }
                ).then(response => {
                    response.json().then((data) => {
                        // success callback
                        if (data.result == 'success') {
                            this.$toasted.success("Successfully sent the voting cards to the voters");
                        }
                        else {
                            this.$toasted.error(data.message);
                        }
                    });
                }, response => {
                    // error callback
                });
            },
        }
    };
</script>
