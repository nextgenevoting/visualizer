<template>
    <v-container grid-list-md>
        <div v-if="this.$store.state.loaded">
            <ContentTitle icon="mdi-settings-box" :title="$t('ElectionAuthority.title')"></ContentTitle>
            <v-layout row wrap>
                <v-flex xs12 sm12>
                    <v-btn-toggle v-model="selectedAuthorityIndex">
                        <v-btn flat v-for="auth in electionAuthorities" :key="auth.id">
                            <v-badge color="red" right>
                                <span slot="badge" v-if="getNumberOfTasks(auth.id) > 0">{{ getNumberOfTasks(auth.id) }}</span>
                                {{ $t('authority') }} {{auth.id + 1}}
                                <v-chip v-if="auth.autoCheck" small color="grey darken-1" text-color="white" v-t="'auto'"></v-chip>
                            </v-badge>
                        </v-btn>
                    </v-btn-toggle>
                </v-flex>
            </v-layout>
            <br>
            <v-layout row wrap>
                <v-flex xs12 sm1><h5 v-t="'tasks'"></h5></v-flex>
                <v-flex sm12 sm11>
                    <v-switch :label="$t('ElectionAuthority.auto_process_tasks')" v-model="autoMode"></v-switch>
                </v-flex>
            </v-layout>
            <CheckBallotTaskPage></CheckBallotTaskPage>
            <ConfirmationTaskPage></ConfirmationTaskPage>
            <MixingPage></MixingPage>
            <DecryptionPage></DecryptionPage>
            <h5 v-t="'data'"></h5>
            <transition-group tag="v-layout" name="highlight" :appear="dataTransition" class="row wrap">
                <v-flex xy12 md6 v-if="status >= 4 && hasAuthorityMixed" key="enc">
                    <DataCard :title="$t('encryptions')" :isMpz=true :expandable=false confidentiality="encrypted">
                        <v-layout row wrap v-for="(encryption, index) in encryptions" :key="index"  style="font-size:16px;">
                            <v-flex xy4 md4>{{ $t('ElectionAuthority.encryption_n', { n: index + 1 }) }}</v-flex>
                            <v-flex xy4 md8>(<BigIntLabel :mpzValue="encryption.a"></BigIntLabel>, <BigIntLabel :mpzValue="encryption.b"></BigIntLabel>)</v-flex>
                        </v-layout>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md6 v-if="status >= 5 && decryptions !== null" key="dec">
                    <DataCard :title="$t('ElectionAuthority.partial_decryptions')" :isMpz=true :expandable=false confidentiality="encrypted">
                        <v-layout row wrap v-for="(decryption, index) in decryptions" :key="index" style="font-size:16px;">
                            <v-flex xy6 md6>{{ $t('ElectionAuthority.partial_decryption_n', { n: index + 1 }) }}</v-flex>
                            <v-flex xy6 md6><BigIntLabel :mpzValue="decryption"></BigIntLabel></v-flex>
                        </v-layout>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md12 key="ballots">
                    <DataCard :title="$t('ballots')" :isMpz=true :expandable=false confidentiality="encrypted">
                        <BallotList :ballots="ballots" :authorityFilter="selectedAuthorityIndex"></BallotList>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4 key="pk">
                    <DataCard :title="$t('public_key')" :isMpz=true :expandable=false confidentiality="public">
                        <BigIntLabel :mpzValue="electionAuthority.publicKey"></BigIntLabel>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4 key="pkshares">
                    <DataCard :title="$t('public_key_share')" :isMpz=true :expandable=false confidentiality="public">
                        <BigIntLabel :mpzValue="electionAuthority.publicKeyShare"></BigIntLabel>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4 key="skshares">
                    <DataCard :title="$t('secret_key_share')" :isMpz=true :expandable=false confidentiality="secret">
                        <BigIntLabel :mpzValue="electionAuthority.secretKeyShare"></BigIntLabel>
                    </DataCard>
                </v-flex>

                <v-flex xy12 md4 v-if="expertMode" key="points">
                    <DataCard :title="$t('points')" :expandable=true confidentiality="secret">
                        {{ $t('ElectionAuthority.points_of_all_voters') }}
                        <ul id="list" slot="expandContent">
                            <li v-for="(voter, index) in electionAuthority.points" :key="voter.id">
                                {{ $t('voter_n', { n: index }) }}
                                <ul id="subList">
                                    <li v-for="(point, index) in voter" :key="index">
                                        x: <BigIntLabel :mpzValue="point[0]"></BigIntLabel>
                                        y: <BigIntLabel :mpzValue="point[1]"></BigIntLabel>
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
        dataTransition: false
      }),
      mounted () {
        this.dataTransition = false
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
        hasAuthorityMixed: {
          get: function () {
            return this.$store.getters.hasAuthorityMixed(this.selectedAuthorityIndex)
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
        },
        numberOfTasks: {
          get: function () {
            return this.$store.getters.getNumberOfTasks(this.selectedAuthorityIndex)
          }
        }
      },
      methods: {
        getNumberOfTasks: function (authority) {
          return this.$store.getters.getNumberOfTasks(authority)
        }
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
    .application--light .chip{
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
