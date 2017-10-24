<template>
    <v-container>
        <h3 class="my-3">Election Authority</h3>

        <v-container fluid grid-list-md>
            <v-layout row wrap>
                <v-flex xs12 sm4>
                    <v-select
                            v-bind:items="data.electionAuthorities"
                            v-model="currentAuthority"
                            item-text="name"
                            item-value="j"
                            single-line
                            bottom
                    ></v-select>
                </v-flex>
                <v-flex sm2></v-flex>
            </v-layout>
        </v-container>

        <h5 class="my-3">Tasks</h5>
        <!--<v-layout row v-if="">
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
        </v-layout>-->

        <h5 class="my-3">Data</h5>
        <v-switch label="Expert mode" v-model="verbose" ></v-switch>

        Public Key:
        <BigIntLabel :mpzValue="data.electionAuthority.publicKey"></BigIntLabel>
        <br>
        Public Key Share:
        <BigIntLabel :mpzValue="data.electionAuthority.publicKeyShare"></BigIntLabel>
        <br>
        Secret Key Share:
        <BigIntLabel :mpzValue="data.electionAuthority.secretKeyShare"></BigIntLabel>
        <br>

        Points:
        <ul id="voterList" v-if="verbose">
            <li v-for="voter in data.electionAuthority.points">
                Voter1
                <ul id="pointList">
                    <li v-for="point in voter">
                        x: <BigIntLabel :mpzValue="point[0]"></BigIntLabel>
                        y: <BigIntLabel :mpzValue="point[1]"></BigIntLabel>
                    </li>
                </ul>
            </li>
        </ul>

    </v-container>
</template>

<script>
export default {
    data: () => ({
        currentAuthority: 0,
        show: false,
        verbose: false
    }),
  computed: {
    data() {
      return {
        id: this.$store.state.Election.electionID,
        status: this.$store.getters.getStatusText,
        electionAuthorities: this.$store.state.ElectionAuthority.electionAuthorities,
        electionAuthority: this.$store.getters.getElectionAuthority(this.currentAuthority),
      };
    },
  },
  created() {
    this.$socket.emit('join', {election: this.$route.params['id'] });
  },
};
</script>
