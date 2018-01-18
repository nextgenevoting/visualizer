<template>
    <v-app id="app">
        <v-navigation-drawer temporary v-model="drawer" absolute>
            <v-list>
                <v-list-tile>
                    <v-list-tile-content>
                        <v-list-tile-title v-t="'menu'"/>
                    </v-list-tile-content>
                </v-list-tile>
                <v-divider></v-divider>
                <template v-for="(item, index) in items">
                    <v-list-tile :href="item.href" :to="{name: item.href}">
                        <v-list-tile-action>
                            <v-icon light v-html="item.icon"></v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>{{ $t(item.title) }}</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                </template>
            </v-list>
        </v-navigation-drawer>

        <header class="siteHeader">
            <v-toolbar class="blue" dark>
                <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
                <v-toolbar-title><img src="/public/nextgenvote2.png" style="width: 152px; height:37px">
                </v-toolbar-title>
                <v-spacer></v-spacer>
                <v-menu offset-y flat>
                    <v-btn icon slot="activator" :title="$t('main.change_language')">
                        <v-icon>mdi-translate</v-icon>
                    </v-btn>
                    <v-list>
                        <v-list-tile v-for="(name, id) in languages" :key="id" @click="changeLanguage(id)">
                            <v-list-tile-title>{{ name }}</v-list-tile-title>
                        </v-list-tile>
                    </v-list>
                </v-menu>
                <v-menu offset-x :close-on-content-click="false" :nudge-width="200" v-model="menu">
                    <v-btn icon slot="activator" :title="$t('settings')">
                        <v-icon>settings</v-icon>
                    </v-btn>
                    <v-card>
                        <v-list>
                            <v-list-tile avatar>
                                <v-list-tile-avatar>
                                    <!--<img src="/public/avatar.jpg" alt="">-->
                                </v-list-tile-avatar>
                                <v-list-tile-content>
                                    <v-list-tile-title>Voteadmin</v-list-tile-title>
                                    <v-list-tile-sub-title>Vote Administrator</v-list-tile-sub-title>
                                </v-list-tile-content>
                                <v-list-tile-action>
                                    <v-btn icon>
                                        <v-icon>logout</v-icon>
                                    </v-btn>
                                </v-list-tile-action>
                            </v-list-tile>
                        </v-list>
                        <v-divider></v-divider>
                        <v-list>
                            <v-list-tile>
                                <v-list-tile-action>
                                    <v-switch color="green" v-model="showConfidentiality"/>
                                </v-list-tile-action>
                                <v-list-tile-title v-t="'main.settings.confidentiality'"/>
                            </v-list-tile>
                            <v-list-tile>
                                <v-list-tile-action>
                                    <v-switch color="green" v-model="fluidLayout"/>
                                </v-list-tile-action>
                                <v-list-tile-title v-t="'main.settings.fluidLayout'"/>
                            </v-list-tile>
                        </v-list>
                        <v-card-actions>
                            <v-spacer/>
                            <v-btn flat @click="menu = false" v-t="'ok'"/>
                        </v-card-actions>
                    </v-card>
                </v-menu>
                <v-btn icon @click="openRepo()" :title="$t('main.view_source_code')">
                    <v-icon>code</v-icon>
                </v-btn>
            </v-toolbar>
            <v-tabs show-arrows slider-color="white" fixed centered icons-and-text grow dark color="blue"
                    v-show="$route.path.includes('/election/')">
                <v-tab ripple :to="{ name: 'electionoverview', params: { electionId: electionId }}"
                       :title="$t('main.overview')">
                    <span class="hidden-sm-and-down">{{ $t('main.overview') }}</span>
                    <v-icon>mdi-view-dashboard</v-icon>
                </v-tab>
                <v-tab ripple :to="{ name: 'electionadmin', params: { electionId: electionId }}"
                       :title="$t('main.election_admin')">
                    <span class="hidden-sm-and-down">{{ $t('main.election_admin') }}</span>
                    <v-badge color="" style="margin-left:-15px">
                        <v-icon slot="badge" v-if="status == 0 || status == 6">mdi-alert-decagram</v-icon>
                        <i class="customicon icon-election-administrator" style="font-size:7px"></i>
                    </v-badge>
                </v-tab>
                <v-tab ripple :to="{ name: 'printingauth', params: {electionId: electionId }}"
                       :title="$t('main.printing_authority')">
                    <span class="hidden-sm-and-down">{{ $t('main.printing_authority') }}</span>
                    <v-badge color="" style="margin-left:-15px">
                        <v-icon slot="badge" v-if="status == 1 || status == 2">mdi-alert-decagram</v-icon>
                        <i class="customicon icon-printing-authority" style="font-size:7px"></i>
                    </v-badge>
                </v-tab>
                <v-tab ripple :to="{ name: 'voter', params: { electionId: electionId, voterId: voterId }}"
                       :disabled="this.$store.getters.status < 1" :title="$t('main.voters')">
                    <span class="hidden-sm-and-down">{{ $t('main.voters') }}</span>
                    <v-badge color="" style="margin-left:-15px">
                        <v-icon slot="badge" v-if="status == 3">mdi-alert-decagram</v-icon>
                        <i class="customicon icon-voter" style="font-size:7px"></i>
                    </v-badge>
                </v-tab>
                <v-tab ripple
                       :to="{ name: 'electionauthority', params: { electionId: electionId, authid: authorityId }}"
                       :title="$t('main.election_authorities')">
                    <span class="hidden-sm-and-down">{{ $t('main.election_authorities') }}</span>
                    <v-badge color="" style="margin-left:-15px">
                        <v-icon slot="badge" v-if="getNumberOfTasksForAllAuthorities > 0">mdi-alert-decagram</v-icon>
                        <i class="customicon icon-election-authorities" style="font-size:7px"></i>
                    </v-badge>
                </v-tab>
                <v-tab ripple :to="{ name: 'bulletinboard', params: { electionId: electionId }}"
                       :title="$t('main.bulletinboard')">
                    <span class="hidden-sm-and-down">{{ $t('main.bulletin_board') }}</span>
                    <v-badge color="" style="margin-left:-15px">

                        <i class="customicon icon-bulletin-board" style="font-size:7px"></i>
                    </v-badge>
                </v-tab>
                <v-tab ripple :to="{ name: 'verifier', params: { electionId: electionId }}" v-if="status >= 7"
                       :title="$t('main.verifier')">
                    <span class="hidden-sm-and-down">{{ $t('main.verifier') }}</span>
                    <v-badge color="" style="margin-left:-5px">
                        <v-icon slot="badge" v-if="status == 7">mdi-alert-decagram</v-icon>
                        <v-icon>mdi-checkbox-marked-outline</v-icon>
                    </v-badge>
                </v-tab>
            </v-tabs>
        </header>

        <main>
            <v-fade-transition mode="out-in">
                <router-view :key="$route.fullPath"></router-view>
            </v-fade-transition>
        </main>

        <v-snackbar error top :timeout="0" v-model="offlineNotification">
            Websocket connection to server lost!
            <v-btn dark flat @click.native="offlineNotification = false" v-t="'close'"></v-btn>
        </v-snackbar>

        <v-snackbar success top :timeout="4000" v-model="onlineNotification">
            Websocket connection established!
            <v-btn dark flat @click.native="onlineNotification = false" v-t="'close'"></v-btn>
        </v-snackbar>
    </v-app>
</template>

<script type="text/babel">
    import {mapGetters, mapState} from 'vuex'

    export default {
      data () {
        return {
          drawer: false,
          items: [{
            href: 'home',
            router: true,
            title: 'home',
            icon: 'home'
          }, {
            href: 'elections',
            router: true,
            title: 'main.election_events',
            icon: 'extension'
          }, {
            href: 'about',
            router: true,
            title: 'main.about',
            icon: 'domain'
          }],
          menu: false
        }
      },
      computed: {
        languages () {
          return this.$root.$i18n._languages
        },
        ...mapState({
          status: 'status'
        }),
        ...mapGetters({
          getNumberOfTasksForAllAuthorities: 'getNumberOfTasksForAllAuthorities'
        }),
        electionId: {
          get () {
            return this.$route.params['electionId']
          }
        },
        authorityId: {
          get () {
            return this.$store.state.selectedAuthority
          }
        },
        voterId: {
          get () {
            return this.$store.state.selectedVoter
          }
        },
        onlineNotification: {
          get () {
            return this.$store.state.connected
          },
          set (value) {
          }
        },
        offlineNotification: {
          get () {
            return !this.$store.state.connected
          },
          set (value) {
          }
        },
        status: {
          get () {
            return this.$store.state.Election.status
          },
          set (value) {
          }
        },

        showConfidentiality: {
          get: function () {
            return this.$store.state.showConfidentiality
          },
          set (value) {
            this.$store.commit('showConfidentiality', value)
          }
        },
        fluidLayout: {
          get: function () {
            return this.$store.state.fluidLayout
          },
          set (value) {
            this.$store.commit('fluidLayout', value)
          }
        }

      },
      methods: {
        changeLanguage (lang) {
          this.$root.$i18n.locale = lang
          this.$store.commit('language', lang)
        },
        openRepo () {
          window.open('https://gitlab.ti.bfh.ch/chvote/demonstrator')
        }
      }
    }
</script>

<style type="text/css">
    @import '../node_modules/nprogress/nprogress.css';
    @import '../node_modules/mdi/css/materialdesignicons.css';
    @import '../node_modules/nprogress/nprogress.css';
    @import 'css/fontello.css';
</style>

<style lang="stylus">
    @import 'css/main.css';
</style>

<style>
    .tabs__wrapper {
        overflow: hidden !important;
    }

    .tabs__container--icons-and-text .tabs__item .icon {
        margin-top: 6px;
    }

    .tabs .badge__badge{
        left: 15px;
    }
</style>
