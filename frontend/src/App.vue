<template>
    <v-app id="app">
        <v-navigation-drawer temporary v-model="drawer">
            <v-list>
                <v-list-tile>
                    <v-list-tile-content>
                        <v-list-tile-title>
                            <span>Menu</span>
                        </v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
                <v-divider></v-divider>
                <template v-for="(item, index) in items">
                    <v-list-tile :href="item.href" :to="{name: item.href}">
                        <v-list-tile-action>
                            <v-icon light v-html="item.icon"></v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title v-html="item.title"></v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                </template>
            </v-list>
        </v-navigation-drawer>
        <header class="siteHeader">
            <v-toolbar class="blue" dark>
                <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
                <v-toolbar-title><img src="/public/logo.png" style="height:22px"></v-toolbar-title>
                <v-spacer></v-spacer>
                <v-btn flat v-if="this.$store.state.selectedVoter != null" @click="changeVoter()">
                    <v-icon>account_circle</v-icon>
                    {{ selectedVoterName }}
                </v-btn>
                <v-menu offset-y>
                    <v-btn icon slot="activator" :title="$t('change_language')">
                        <v-icon>mdi-translate</v-icon>
                    </v-btn>
                    <v-list>
                        <v-list-tile v-for="(name, id) in languages" :key="id" @click="changeLanguage(id)">
                            <v-list-tile-title>{{ name }}</v-list-tile-title>
                        </v-list-tile>
                    </v-list>
                </v-menu>
                <v-menu
                        offset-x
                        :close-on-content-click="false"
                        :nudge-width="200"
                        v-model="menu"
                >
                    <v-btn icon slot="activator">
                        <v-icon>settings</v-icon>
                    </v-btn>
                    <v-card>
                        <v-list>
                            <v-list-tile avatar>
                                <v-list-tile-avatar>
                                    <img src="/public/avatar.jpg" alt="">
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
                                    <v-switch color="green" v-model="expertMode"></v-switch>
                                </v-list-tile-action>
                                <v-list-tile-title>Expert mode</v-list-tile-title>
                            </v-list-tile>
                            <v-list-tile>
                                <v-list-tile-action>
                                    <v-switch color="green" v-model="showConfidentiality"></v-switch>
                                </v-list-tile-action>
                                <v-list-tile-title>Show confidentiality</v-list-tile-title>
                            </v-list-tile>
                        </v-list>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn flat @click="menu = false">OK</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-menu>
                <v-btn icon @click.native.stop="openGithub()">
                    <v-icon>home</v-icon>
                </v-btn>
            </v-toolbar>
            <v-tabs dark grow icons centered>
                <v-tabs-bar class="blue" v-show="$route.path.includes('/election/') ? true : false">
                    <v-tabs-slider color="white"></v-tabs-slider>
                    <v-tabs-item ripple :to="{ name: 'electionoverview', params: {id: $route.params['id'] }}">
                        <v-icon>mdi-view-dashboard</v-icon>
                        Overview
                    </v-tabs-item>
                    <v-tabs-item ripple :to="{ name: 'electionadmin', params: {id: $route.params['id'] }}">
                        <v-badge color="">
                            <v-icon slot="badge" dark v-if="status == 0">mdi-alert-decagram</v-icon>
                            <v-icon>mdi-account-key</v-icon>
                        </v-badge>
                        Election Admin
                    </v-tabs-item>
                    <v-tabs-item ripple :to="{ name: 'printingauth', params: {id: $route.params['id'] }}">
                        <v-badge color="">
                            <v-icon slot="badge" dark v-if="status == 1">mdi-alert-decagram</v-icon>
                            <v-icon>mdi-printer</v-icon>
                        </v-badge>
                        Printing Auth.
                    </v-tabs-item>
                    <v-tabs-item ripple :to="{ name: 'voter', params: {id: $route.params['id'] }}"
                                 :disabled="this.$store.getters.getStatus < 1">
                        <v-badge color="">
                            <v-icon slot="badge" dark v-if="status == 3">mdi-alert-decagram</v-icon>
                            <v-icon>mdi-account</v-icon>
                        </v-badge>
                        Voters
                    </v-tabs-item>
                    <v-tabs-item ripple :to="{ name: 'electionauthority', params: {id: $route.params['id'] }}">
                        <v-badge class="">
                            <v-icon slot="badge" dark v-if="status == 5">mdi-alert-decagram</v-icon>
                            <v-icon>mdi-settings-box</v-icon>
                        </v-badge>
                        Election Authorities
                    </v-tabs-item>
                    <v-tabs-item ripple :to="{ name: 'bulletinboard', params: {id: $route.params['id'] }}">
                        <v-icon>mdi-bulletin-board</v-icon>
                        Bulletin Board
                    </v-tabs-item>
                </v-tabs-bar>
            </v-tabs>
        </header>
        <main>
            <v-fade-transition mode="out-in">
                <router-view></router-view>
            </v-fade-transition>
        </main>

        <v-snackbar error top :timeout="0" v-model="offlineNotification">
            Websocket connection to server lost!
            <v-btn dark flat @click.native="offlineNotification = false">Close</v-btn>
        </v-snackbar>

        <v-snackbar success top :timeout="4000" v-model="onlineNotification">
            Websocket connection established!
            <v-btn dark flat @click.native="onlineNotification = false">Close</v-btn>
        </v-snackbar>
        <SelectVoterDialog></SelectVoterDialog>
    </v-app>

</template>

<i18n>
en:
  change_language: Change language
  menu:
    title: Menu
    home: Home
    elections: Elections
    about: About
  close: Close
  settings:
    title: Settings
    status: Status on all pages
    confidentiality: Show confidentiality
  open_repo: Open BFH Gitlab repository
de:
  change_language: Sprache ändern
  menu:
    title: Menü
    home: Homepage
    elections: Wahlen
    about: Über
  close: Schliessen
  settings:
    title: Einstellungen
    status: Status auf allen Seiten
    confidentiality: Vertraulichkeit anzeigen
  open_repo: BFH Gitlab Repository öffnen

</i18n>

<script type="text/babel">
    import SelectVoterDialog from './pages/SelectVoterDialog.vue';

    export default {
        data() {
            return {
                drawer: false,
                items: [{
                    href: 'home',
                    router: true,
                    title: 'Home',
                    icon: 'home',
                }, {
                    href: 'elections',
                    router: true,
                    title: 'Elections',
                    icon: 'extension',
                }, {
                    href: 'about',
                    router: true,
                    title: 'About',
                    icon: 'domain',
                }],
                menu: false,
                voterDialog: false,
                languages: {
                    'en': 'English',
                    'de': 'Deutsch',
                },
            };
        },
        computed: {

            onlineNotification: {
                get() {
                    return this.$store.state.connected
                },
                set(value) {
                }
            },
            offlineNotification: {
                get() {
                    return !this.$store.state.connected
                },
                set(value) {
                }
            },
            status: {
                get() {
                    return this.$store.state.Election.status
                },
                set(value) {
                }
            },

            showConfidentiality: {
                get() {
                    return this.$store.state.showConfidentiality;
                },
                set(value) {
                    this.$store.state.showConfidentiality = value;
                }
            },
            expertMode: {
                get() {
                    return this.$store.state.expertMode;
                },
                set(value) {
                    this.$store.state.expertMode = value;
                }
            },
            selectedVoterName: {
                get() {
                    if (this.$store.state.selectedVoter != null) {
                        return this.$store.getters.getVoter(this.$store.state.selectedVoter).name;
                    } else {
                        return '';
                    }
                },
                set(value) {
                    this.$store.commit("changeSelectedVoter", value);
                }
            },
        },
        methods: {
            openGithub: function () {
                window.open('https://chvote.ch');
            },
            changeVoter: function () {
                this.$store.commit("voterDialog", true);
            },
            changeLanguage(lang) {
                this.$root.$i18n.locale = lang
                this.$store.state.language = lang
            }
        },
        components: {
            'SelectVoterDialog': SelectVoterDialog
        }
    };

</script>

<style type="text/css">
    @import '../node_modules/nprogress/nprogress.css';
    @import '../node_modules/mdi/css/materialdesignicons.css';
    @import '../node_modules/nprogress/nprogress.css';
</style>

<style lang="stylus">
    @import '../node_modules/vuetify/src/stylus/main';
    @import 'css/main.css';
</style>
