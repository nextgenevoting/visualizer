<template>
    <v-container grid-list-md>

        <div class="layout row wrap">
            <div class="contentHeader">
                <i class="mdi icon mdi-bulletin-board"></i>
            </div>
            <h3 class="my-3">Bulletin Board</h3>
        </div>

        <v-layout row wrap>

            <v-flex xy12 md4>
                <DataCard title="Unique Election Identifier" :expandable=false confidentiality="public">{{data.id}}
                </DataCard>
            </v-flex>

            <v-flex xy12 md4>
                <DataCard title="Status" :expandable=false confidentiality="public">{{data.status}}</DataCard>
            </v-flex>

            <v-flex xy12 md4>
                <DataCard title="Public Key" :isMpz=true :expandable=false confidentiality="public">
                    <BigIntLabel :mpzValue="data.publicKey"></BigIntLabel>
                </DataCard>
            </v-flex>

            <v-flex xy12 md4>
                <DataCard title="Candidates" :expandable=false confidentiality="public">{{data.candidates}}</DataCard>
            </v-flex>

            <v-flex xy12 md4>
                <DataCard title="Counting Circles" :expandable=false confidentiality="public">{{data.countingCircles}}
                </DataCard>
            </v-flex>

            <v-flex xy12 md4>
                <DataCard title="Selections" :expandable=false confidentiality="public">{{data.numberOfSelections}}
                </DataCard>
            </v-flex>

            <v-flex xy12 md4>
                <DataCard title="Voters" :expandable=false confidentiality="public">{{data.voters}}</DataCard>
            </v-flex>


            <v-flex xy12 md4>
                <DataCard title="Public Voting Credentials" :expandable=true confidentiality="public">
                    Voters public voting credentials
                    <ul id="subList" slot="expandContent">
                        <li v-for="(item, key, index) in data.publicVotingCredentials">
                            {{ index}}
                            <ul>
                                X:
                                <BigIntLabel :mpzValue="item[0]"></BigIntLabel>
                                Y:
                                <BigIntLabel :mpzValue="item[1]"></BigIntLabel>
                            </ul>

                        </li>
                    </ul>
                </DataCard>
            </v-flex>

        </v-layout>

    </v-container>
</template>

<script>
    export default {
        data: () => ({
            showCredentials: false
        }),
        computed: {
            data() {
                return {
                    id: this.$store.state.Election.electionID,
                    status: this.$store.getters.getStatusText,
                    publicKey: this.$store.state.BulletinBoard.publicKey,
                    voters: this.$store.state.BulletinBoard.voters,
                    candidates: this.$store.state.BulletinBoard.candidates,
                    publicVotingCredentials: this.$store.state.BulletinBoard.publicVotingCredentials,
                    numberOfSelections: this.$store.state.BulletinBoard.numberOfSelections,
                    countingCircles: this.$store.state.BulletinBoard.countingCircles,
                }
            }
        },
        created() {
            this.$socket.emit('join', {'election': this.$route.params["id"]});
        }
    };
</script>
