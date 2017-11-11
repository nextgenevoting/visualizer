<template>
    <v-container grid-list-md>
        <div v-if="this.$store.state.loaded">
            <ContentTitle icon="mdi-settings-box" title="Election Authorities"></ContentTitle>
            <v-layout row>

                <v-flex xs12 sm12>
                    <v-btn-toggle v-model="selectedAuthorityIndex">
                        <v-btn flat v-for="auth in electionAuthorities" :key="auth.id">
                            <v-badge color="red" right>
                                <span slot="badge" v-if="auth.checkBallotTasks.length > 0">{{ auth.checkBallotTasks.length }}</span>
                                Authority {{auth.id + 1}}  <v-chip v-if="auth.autoCheck" small outline color="secondary">auto</v-chip>
                            </v-badge>
                        </v-btn>
                    </v-btn-toggle>
                </v-flex>
            </v-layout>
            <br>
            <v-layout row>
                <v-flex xs12 sm1><h5 class="">Tasks</h5></v-flex>
                <v-flex sm12 sm11>
                    <v-switch label="Automatic process tasks" v-model="autoMode"></v-switch>
                </v-flex>
            </v-layout>
            <CheckBallotTaskPage></CheckBallotTaskPage>
            <ConfirmationTaskPage></ConfirmationTaskPage>
            <MixingPage></MixingPage>
            <DecryptionPage></DecryptionPage>
            <h5 class="">Data</h5>
            <transition-group tag="v-layout" name="highlight" :appear="dataTransition" class="row wrap">
                <v-flex xy12 md6 v-if="status >= 5 && decryptions !== null" key="dec">
                    <DataCard title="Partial Decryptions" :isMpz=true :expandable=false confidentiality="public">
                        <v-layout row v-for="(decryption, index) in decryptions">
                            <v-flex xy6 md6>Partial Decryption {{index+1}}</v-flex>
                            <v-flex xy6 md6><BigIntLabel :mpzValue="decryption"></BigIntLabel></v-flex>
                        </v-layout>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md6 v-if="status >= 4 && hasAuthorityShuffled" key="enc">
                    <DataCard title="Encryptions" :isMpz=true :expandable=false confidentiality="public">
                        <v-layout row v-for="(encryption, index) in encryptions">
                            <v-flex xy4 md6>Encryption {{index+1}}</v-flex>
                            <v-flex xy4 md6><BigIntLabel :mpzValue="encryption.a"></BigIntLabel></v-flex>
                            <v-flex xy4 md6><BigIntLabel :mpzValue="encryption.b"></BigIntLabel></v-flex>
                        </v-layout>
                    </DataCard>
                </v-flex>


                <v-flex xy12 md12 key="ballots">
                    <DataCard title="Ballots" :isMpz=true :expandable=false confidentiality="encrypted">

                        <transition-group tag="v-expansion-panel" name="highlight" class="expansion-panel--popout" :appear="ballotTransition">
                            <v-expansion-panel-content v-for="ballot in ballots" :key="ballot.ballot.x_hat">
                                <div slot="header">Ballot of voter {{ballot.voterId}}
                                    <transition name="highlight">
                                        <v-chip left label outline color="green" v-if="ballot.confirmation !== null">Confirmed</v-chip>
                                    </transition>
                                </div>
                                <v-card>
                                    <v-card-text class="grey lighten-3">
                                        <v-layout row>
                                            <v-flex xy2 md2>Encrypted selections:</v-flex>
                                            <v-flex x10 md10>
                                                <span v-for="elgamalEncryption in ballot.ballot.a_bold">
                                                (<BigIntLabel :mpzValue="elgamalEncryption[0]"></BigIntLabel>,
                                                <BigIntLabel :mpzValue="elgamalEncryption[1]"></BigIntLabel>)
                                                </span>
                                            </v-flex>
                                        </v-layout>
                                        <v-layout row>
                                            <v-flex xy2 md2>Public voter credential:</v-flex>
                                            <v-flex xy10 md10><BigIntLabel :mpzValue="ballot.ballot.x_hat"></BigIntLabel></v-flex>
                                        </v-layout>
                                        <v-layout row>
                                            <v-flex xy2 md2>Ballot-Proof:</v-flex>
                                            <v-flex x10 md10>
                                                <span v-for="a in ballot.ballot.pi">
                                                <p v-for="i in a"><BigIntLabel :mpzValue="i"></BigIntLabel></p>
                                                </span>
                                            </v-flex>
                                        </v-layout>
                                    </v-card-text>
                                </v-card>
                            </v-expansion-panel-content>
                        </transition-group>

                    </DataCard>
                </v-flex>

                <v-flex xy12 md4 key="pk">
                    <DataCard title="Public Key" :isMpz=true :expandable=false confidentiality="public">
                        <BigIntLabel :mpzValue="electionAuthority.publicKey"></BigIntLabel>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4 key="pkshares">
                    <DataCard title="Public Key Share" :isMpz=true :expandable=false confidentiality="public">
                        <BigIntLabel :mpzValue="electionAuthority.publicKeyShare"></BigIntLabel>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4 key="skshares">
                    <DataCard title="Secret Key Share" :isMpz=true :expandable=false confidentiality="secret">
                        <BigIntLabel :mpzValue="electionAuthority.secretKeyShare"></BigIntLabel>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4 v-if="expertMode" key="points">
                    <DataCard title="Points" :expandable=true confidentiality="secret">
                        Points of all voters
                        <ul id="list" slot="expandContent">
                            <li v-for="(voter, index) in electionAuthority.points" :key="voter.id">
                                Voter {{ index}}
                                <ul id="subList">
                                    <li v-for="(point, index) in voter" :key="index">
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
            </transition-group>
        </div>
        <div v-else>
            <LoadingOverlay></LoadingOverlay>
        </div>
    </v-container>
</template>

<script>
    import { mapState, mapGetters } from 'vuex'
    import joinRoomMixin from '../../mixins/joinRoomMixin.js'

    export default {
      mixins: [joinRoomMixin],
      data: () => ({
        show: false,
        ballotTransition: false,
        dataTransition: false
      }),
      mounted () {
        this.dataTransition = false
        this.ballotTransition = false
        this.$store.commit('selectedAuthority', this.$route.params.authid)
      },
      computed: {
        ...mapState({
          electionAuthorities: state => state.ElectionAuthority.electionAuthorities,
          expertMode: state => state.BulletinBoard.expertMode
        }),
        ...mapGetters({
          electionId: 'electionId',
          status: 'status'
        }),
        selectedAuthorityIndex: {
          get: function () {
            return parseInt(this.$route.params['authid'])
          },
          set: function (newAuthId) {
            if (newAuthId !== null) {
              this.$store.commit('selectedAuthority', newAuthId)
              this.$router.push({name: 'electionauthority', params: {electionId: this.$route.params['electionId'], authid: newAuthId}})
            }
          }
        },
        electionAuthority: {
          get: function () {
            return this.$store.getters.getElectionAuthority(this.selectedAuthorityIndex)
          }
        },
        ballots: {
          get: function () {
            return this.$store.getters.getBallotsAndConfirmations(this.selectedAuthorityIndex)
          }
        },
        confirmations: {
          get: function () {
            return this.$store.getters.getConfirmations(this.selectedAuthorityIndex)
          }
        },
        autoMode: {
          get: function () {
            return this.electionAuthority.autoCheck
          },
          set: function (value) {
            this.$store.dispatch('setAutoMode', {electionId: this.$route.params['electionId'], electionAuthorityId: this.selectedAuthorityIndex, newValue: value})
          }
        },
        hasAuthorityShuffled: {
          get: function () {
            return this.$store.getters.hasAuthorityShuffled(this.selectedAuthorityIndex)
          }
        },
        decryptions: {
          get: function () {
            return this.$store.getters.getDecryptionsForAuthority(this.selectedAuthorityIndex)
          }
        },
        encryptions: {
          get: function () {
            return this.$store.getters.getEncryptionsForAuthority(this.selectedAuthorityIndex)
          }
        }
      },
      methods: {
      }
    }
</script>

<style>
    .btn-toggle {
        width: 100%;
        background-color: transparent !important;
        margin-top: -5px !important;
        opacity: 1;
    }

    .btn-toggle .btn {
        width: 33%;
        border-radius: 4px !important;
        opacity: 1;
    }

    .btn-toggle--selected {
        box-shadow: none;
    }

    .highlight-enter-active {
        animation: highlight 2.5s;
    }

    .btn-toggle .badge{
        font-weight: 300;
    }

    .btn--active .badge{
        font-weight: 600;
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
</style>