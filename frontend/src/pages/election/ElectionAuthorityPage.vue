<template>
    <v-container grid-list-md :fluid="fluidLayout">
        <div v-if="this.$store.state.loaded">
            <ContentTitle customicon="customicon icon-election-authorities" :title="$t('ElectionAuthority.title')"></ContentTitle>
            <v-layout row wrap>
                <v-flex xs12 sm12>
                    <v-btn-toggle v-model="selectedAuthorityIndex">
                        <v-btn flat v-for="auth in electionAuthorities" :key="auth.id">
                            <v-badge color="red" right>
                                <span slot="badge" v-if="getNumberOfTasks(auth.id) > 0">{{ getNumberOfTasks(auth.id) }}</span>
                                {{ $t('authority') }} {{auth.id + 1}}
                                <v-chip small v-if="auth.autoCheck" color="grey darken-1" text-color="white">{{ $t('auto') }}</v-chip>
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
            <h5 v-t="'data'" style="margin-top: 14px;"></h5>
            <transition-group tag="v-layout" name="highlight" :appear="dataTransition" class="row wrap">
                <v-flex xs12 md6 v-if="status >= 4 && hasAuthorityMixed" key="enc">
                    <DataCard :title="$t('encryptions')" :tooltip="$t('encryptions_tooltip')" :isMpz=true :expandable=false confidentiality="encrypted">
                        <v-layout row wrap v-for="(encryption, index) in encryptions" :key="index"  style="font-size:16px;">
                            <v-flex xs4 md4>{{ $t('ElectionAuthority.encryption_n', { n: index + 1 }) }}</v-flex>
                            <v-flex xs4 md8>(<BigIntLabel :mpzValue="encryption.a"></BigIntLabel>, <BigIntLabel :mpzValue="encryption.b"></BigIntLabel>)</v-flex>
                        </v-layout>
                    </DataCard>
                </v-flex>

                <v-flex xs12 md6 v-if="status >= 5 && decryptions !== null" key="dec">
                    <DataCard :title="$t('ElectionAuthority.partial_decryptions')" :tooltip="$t('ElectionAuthority.partial_decryptions_tooltip')" :isMpz=true :expandable=false confidentiality="encrypted">
                        <v-layout row wrap v-for="(decryption, index) in decryptions" :key="index" style="font-size:16px;">
                            <v-flex xs6 md6>{{ $t('ElectionAuthority.partial_decryption_n', { n: index + 1 }) }}</v-flex>
                            <v-flex xs6 md6><BigIntLabel :mpzValue="decryption"></BigIntLabel></v-flex>
                        </v-layout>
                    </DataCard>
                </v-flex>

                <v-flex xs12 md12 key="ballots">
                    <DataCard :title="$t('ballotlist')" :tooltip="$t('ballotlist_tooltip')" :isMpz=true :expandable=false confidentiality="encrypted">
                        <BallotList :ballots="ballots" :authorityFilter="selectedAuthorityIndex"></BallotList>
                    </DataCard>
                </v-flex>

                <v-flex xs12 sm4 md4 key="pk">
                    <DataCard :title="$t('public_key')" :tooltip="$t('public_key_tooltip')" :isMpz=true :expandable=false confidentiality="public">
                        <BigIntLabel :mpzValue="electionAuthority.publicKey"></BigIntLabel>
                    </DataCard>
                </v-flex>

                <v-flex xs12 sm4 md4 key="pkshares">
                    <DataCard :title="$t('public_key_share')" :tooltip="$t('public_key_share_tooltip')"  :isMpz=true :expandable=false confidentiality="public">
                        <BigIntLabel :mpzValue="electionAuthority.publicKeyShare"></BigIntLabel>
                    </DataCard>
                </v-flex>

                <v-flex xs12 sm4 md4 key="skshares">
                    <DataCard :title="$t('secret_key_share')" :tooltip="$t('secret_key_share_tooltip')" :isMpz=true :expandable=false confidentiality="secret">
                        <BigIntLabel :mpzValue="electionAuthority.secretKeyShare"></BigIntLabel>
                    </DataCard>
                </v-flex>

                <v-flex xs12 md12 key="voterData">
                    <DataCard :title="$t('electorate_data')" :tooltip="$t('electorate_data_tooltip')" :expandable=true confidentiality="secret">
                        {{ $t('ElectionAuthority.election_data_content') }}
                        <ul id="list" slot="expandContent">
                            <v-layout row wrap>
                                <v-flex xs1 md1>{{$t('voter')}}</v-flex>
                                <v-flex xs3 md3>{{$t('ElectionAuthority.points')}}</v-flex>
                                <v-flex xs4 md4>{{$t('ElectionAuthority.partial_public_voting_credentials')}}</v-flex>
                                <v-flex xs4 md4>{{$t('ElectionAuthority.partial_secret_voting_credentials')}}</v-flex>
                            </v-layout>
                            <li v-for="(voter, index) in electionAuthority.points" :key="voter.id">
                                <v-layout row wrap>
                                    <v-flex xs1 md1>
                                {{ $t('voter_n', { n: index+1 }) }}
                                    </v-flex>
                                    <v-flex xs3 md3>
                                        <ul id="subList">
                                            <li v-for="(point, index) in voter" :key="index">
                                                <BigIntLabel :mpzValue="point[0]"></BigIntLabel>,
                                                <BigIntLabel :mpzValue="point[1]"></BigIntLabel>
                                            </li>
                                        </ul>
                                    </v-flex>
                                    <v-flex xs4 md4>
                                        (<template v-for="(value, i) in electionAuthority.partialPublicVotingCredentials[index]">
                                          <BigIntLabel :mpzValue="value" /><span v-if="i < electionAuthority.partialPublicVotingCredentials[index].length - 1">, </span>
                                        </template>)
                                    </v-flex>
                                    <v-flex xs4 md4>
                                        (<BigIntLabel :mpzValue="electionAuthority.partialSecretVotingCredentials[index][0]" />,
                                        <BigIntLabel :mpzValue="electionAuthority.partialSecretVotingCredentials[index][1]" />,
                                        <ByteArrayLabel :value="electionAuthority.partialSecretVotingCredentials[index][2]" />,
                                        (<template v-for="(value, i) in electionAuthority.partialSecretVotingCredentials[index][3]">
                                          <ByteArrayLabel :value="value" /><span v-if="i < electionAuthority.partialSecretVotingCredentials[index][3].length - 1">, </span>
                                        </template>))
                                    </v-flex>
                                </v-layout>
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
          electionAuthorities: state => state.ElectionAuthority.electionAuthorities
        }),
        ...mapGetters({
          electionId: 'electionId',
          status: 'status',
          fluidLayout: 'fluidLayout'
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
