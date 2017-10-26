<template>
    <v-container>

        <div class="layout row wrap">
            <div class="contentHeader">
                <i class="mdi icon mdi-bulletin-board"></i>
            </div>
            <h3 class="my-3">Bulletin Board</h3>
        </div>

        <v-container grid-list-md text-xs-center>
            <v-layout row wrap>

                <v-flex xy12 md4>
                    <DataCard title="Unique Election Identifier" :value="data.id" :isMpz=false :expandable=false confidentiality="public"></DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Status" :value="data.status" :isMpz=false :expandable=false confidentiality="public"></DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Public Key" :value="data.publicKey" :isMpz=true :expandable=false confidentiality="public"></DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Candidates" :value="data.candidates" :isMpz=false :expandable=false confidentiality="public"></DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Counting Circles" :value="data.countingCircles" :isMpz=false :expandable=false confidentiality="public"></DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Selections" :value="data.numberOfSelections" :isMpz=false :expandable=false confidentiality="public"></DataCard>
                </v-flex>

                <v-flex xy12 md4>
                    <DataCard title="Voters" :value="data.voters":isMpz=false :expandable=false confidentiality="public"></DataCard>
                </v-flex>


                <v-flex xy12 md4>
                    <DataCard title="Public Voting Credentials" value="Voters public voting credentials" :isMpz=false :expandable=true confidentiality="public">
                        <ul id="subList">
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
        <br>
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
