<template>
    <v-container grid-list-md>
        <div class="layout row wrap">
            <div class="contentHeader">
                <i class="mdi icon mdi-settings-box"></i>
            </div>
            <h3 class="my-3">Election Authorities</h3>
        </div>

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
        <v-layout row v-if="1==0">
            <v-flex xs12 sm12>
                <v-card>

                    <v-card-title primary-title>
                        <div>
                            <div class="headline">New ballot submitted</div>
                            <span class="grey--text">Please check the ballot and respond to the query</span>
                        </div>
                    </v-card-title>
                    <v-card-actions>
                        <v-btn flat>Check</v-btn>
                        <v-btn flat color="blue">Respond</v-btn>
                        <v-spacer></v-spacer>
                        <v-btn icon @click.native="show = !show">
                            <v-icon>{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
                        </v-btn>
                    </v-card-actions>
                    <v-slide-y-transition>
                        <v-card-text v-show="show">
                            Show additional information about the ballot
                        </v-card-text>
                    </v-slide-y-transition>
                </v-card>
            </v-flex>
        </v-layout>

        <br>
        <br>
        <h5 class="">Data</h5>

        <v-layout row wrap>

            <v-flex xy12 md4>
                <DataCard title="Public Key" :isMpz=true :expandable=false confidentiality="public"><BigIntLabel :mpzValue="data.electionAuthority.publicKey"></BigIntLabel></DataCard>
            </v-flex>

            <v-flex xy12 md4>
                <DataCard title="Public Key Share" :isMpz=true :expandable=false confidentiality="public"><BigIntLabel :mpzValue="data.electionAuthority.publicKeyShare"></BigIntLabel></DataCard>
            </v-flex>

            <v-flex xy12 md4>
                <DataCard title="Secret Key Share" :isMpz=true :expandable=false confidentiality="secret"><BigIntLabel :mpzValue="data.electionAuthority.secretKeyShare"></BigIntLabel></DataCard>
            </v-flex>

            <v-flex xy12 md4 v-if="data.expertMode">
                <DataCard title="Points" :expandable=true confidentiality="secret">
                    Points of all voters
                    <ul id="subList" slot="expandContent">
                        <li v-for="(voter, index) in data.electionAuthority.points">
                            Voter {{ index}}
                            <ul id="subList">
                                <li v-for="point in voter">
                                    x: <BigIntLabel :mpzValue="point[0]"></BigIntLabel>
                                    y: <BigIntLabel :mpzValue="point[1]"></BigIntLabel>
                                </li>
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
        currentAuthority: 0,
        show: false,
    }),
  computed: {
    data() {
      return {
        id: this.$store.state.Election.electionID,
        status: this.$store.getters.getStatusText,
        electionAuthorities: this.$store.state.ElectionAuthority.electionAuthorities,
        electionAuthority: this.$store.getters.getElectionAuthority(this.currentAuthority),
        expertMode: this.$store.state.expertMode,
      };
    },
  },
  created() {
    this.$socket.emit('join', {election: this.$route.params['id'] });
  },
};
</script>

<style>
.btn-toggle{
    width: 100%;
}

.btn-toggle .btn{
    width: 33%;
}
</style>