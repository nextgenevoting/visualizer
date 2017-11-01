<template>
    <v-container grid-list-md>
        <div v-if="this.$store.state.loaded">
            <ContentTitle icon="mdi-bulletin-board" title="Bulletin Board"></ContentTitle>

            <v-layout row wrap>

                <v-flex xy12 md4>
                    <DataCard title="Unique Election Identifier" :expandable=false confidentiality="public">{{electionId}}
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
            showCredentials: false
        }),
        computed: {
            ...mapState({
                voters: state => state.BulletinBoard.voters,
                countingCircles: state => state.BulletinBoard.countingCircles,
                publicVotingCredentials: state => state.BulletinBoard.publicVotingCredentials,
                numberOfSelections: state => state.BulletinBoard.numberOfSelections,
                candidates: state => state.BulletinBoard.candidates,
                publicKey: state => state.BulletinBoard.publicKey
            }),
            ...mapGetters({
                electionId: "electionId",
                status: "statusText",
            })
        },
        created() {
            if (this.$store.getters.joinedElectionId !== this.$route.params['id'])
                this.$socket.emit('join', {election: this.$route.params['id']});
        }
    };
</script>
