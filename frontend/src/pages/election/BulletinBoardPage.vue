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
                <DataCard title="Unique Election Identifier" :expandable=false confidentiality="public">{{id}}
                </DataCard>
            </v-flex>

            <v-flex xy12 md4>
                <DataCard title="Status" :expandable=false confidentiality="public">{{status}}</DataCard>
            </v-flex>

            <v-flex xy12 md4>
                <DataCard title="Public Key" :isMpz=true :expandable=false confidentiality="public">
                    <BigIntLabel :mpzValue="publicKey"></BigIntLabel>
                </DataCard>
            </v-flex>

            <v-flex xy12 md4>
                <DataCard title="Candidates" :expandable=false confidentiality="public">{{candidates}}</DataCard>
            </v-flex>

            <v-flex xy12 md4>
                <DataCard title="Counting Circles" :expandable=false confidentiality="public">{{countingCircles}}
                </DataCard>
            </v-flex>

            <v-flex xy12 md4>
                <DataCard title="Selections" :expandable=false confidentiality="public">{{numberOfSelections}}
                </DataCard>
            </v-flex>

            <v-flex xy12 md4>
                <DataCard title="Voters" :expandable=false confidentiality="public">{{voters}}</DataCard>
            </v-flex>


            <v-flex xy12 md4>
                <DataCard title="Public Voting Credentials" :expandable=true confidentiality="public">
                    Voters public voting credentials
                    <ul id="subList" slot="expandContent">
                        <li v-for="(item, key, index) in publicVotingCredentials">
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
            id: {
                get: function(){
                    return this.$store.getters.electionId;
                }
            },
            status: {
                get: function(){
                    return this.$store.getters.statusText;
                }
            },
            publicKey: {
                get: function(){
                    return this.$store.state.BulletinBoard.publicKey;
                }
            },
            voters: {
                get: function(){
                    return this.$store.state.BulletinBoard.voters;
                }
            },
            candidates: {
                get: function(){
                    return this.$store.state.BulletinBoard.candidates;
                }
            },
            numberOfSelections: {
                get: function(){
                    return this.$store.state.BulletinBoard.numberOfSelections;
                }
            },
            countingCircles: {
                get: function(){
                    return this.$store.state.BulletinBoard.countingCircles;
                }
            },
            publicVotingCredentials: {
                get: function(){
                    return this.$store.state.BulletinBoard.publicVotingCredentials;
                }
            },
        },
        created() {
            if(this.$store.getters.joinedElectionId !== this.$route.params['id'])
                this.$socket.emit('join', { election: this.$route.params['id'] });
        }
    };
</script>
