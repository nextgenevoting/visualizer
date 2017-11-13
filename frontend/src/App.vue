<template>
  <v-app id="app">
    <v-navigation-drawer temporary v-model="drawer">
      <v-list>
        <v-list-tile>
          <v-list-tile-content>
            <v-list-tile-title v-t="'menu.title'" />
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
        <v-toolbar-title><img src="/public/logo.png" style="height:22px"></v-toolbar-title>
        <v-spacer></v-spacer>
        <v-menu offset-y flat>
          <v-btn icon slot="activator" :title="$t('change_language')">
            <v-icon>mdi-translate</v-icon>
          </v-btn>
          <v-list>
            <v-list-tile v-for="(name, id) in languages" :key="id" @click="changeLanguage(id)">
              <v-list-tile-title>{{ name }}</v-list-tile-title>
            </v-list-tile>
          </v-list>
        </v-menu>
        <v-menu offset-x :close-on-content-click="false" :nudge-width="200" v-model="menu">
          <v-btn icon slot="activator">
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
                  <v-switch color="green" v-model="expertMode" />
                </v-list-tile-action>
                <v-list-tile-title v-t="'settings.expert'" />
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-action>
                  <v-switch color="green" v-model="showConfidentiality" />
                </v-list-tile-action>
                <v-list-tile-title v-t="'settings.confidentiality'" />
              </v-list-tile>
            </v-list>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn flat @click="menu = false" v-t="'settings.ok'" />
            </v-card-actions>
          </v-card>
        </v-menu>
      </v-toolbar>
      <v-tabs dark grow icons centered :scrollable="false">
        <v-tabs-bar class="blue" v-show="$route.path.includes('/election/') ? true : false">
          <v-tabs-slider color="white"></v-tabs-slider>
          <v-tabs-item ripple :to="{ name: 'electionoverview', params: {electionId: electionId}}">
            <v-icon>mdi-view-dashboard</v-icon>
            Overview
          </v-tabs-item>
          <v-tabs-item ripple :to="{ name: 'electionadmin', params: {electionId: electionId }}">
            <v-badge color="">
              <v-icon slot="badge" dark v-if="status == 0 || status == 6">mdi-alert-decagram</v-icon>
              <v-icon>mdi-account-key</v-icon>
            </v-badge>
            Election Admin
          </v-tabs-item>
          <v-tabs-item ripple :to="{ name: 'printingauth', params: {electionId: electionId }}">
            <v-badge color="">
              <v-icon slot="badge" dark v-if="status == 1">mdi-alert-decagram</v-icon>
              <v-icon>mdi-printer</v-icon>
            </v-badge>
            Printing Auth.
          </v-tabs-item>
          <v-tabs-item ripple :to="{ name: 'voter', params: {electionId: electionId }}" :disabled="this.$store.getters.status < 1">
            <v-badge color="">
              <v-icon slot="badge" dark v-if="status == 3">mdi-alert-decagram</v-icon>
              <v-icon>mdi-account</v-icon>
            </v-badge>
            Voter
          </v-tabs-item>
          <v-tabs-item ripple :to="{ name: 'electionauthority', params: {electionId: electionId, authid: authorityId}}">
            <v-badge color="">
              <v-icon slot="badge" dark v-if="status == 5">mdi-alert-decagram</v-icon>
              <v-icon>mdi-settings-box</v-icon>
            </v-badge>
            Election Authorities
          </v-tabs-item>
          <v-tabs-item ripple :to="{ name: 'bulletinboard', params: {electionId: electionId }}">
            <v-icon>mdi-bulletin-board</v-icon>
            Bulletin Board
          </v-tabs-item>
        </v-tabs-bar>
      </v-tabs>
    </header>

    <main>
      <v-fade-transition mode="out-in">
        <router-view :key="$route.params['electionId'] + $route.params['authid']"></router-view>
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
  </v-app>
</template>

<script type="text/babel">
export default {
  data () {
    return {
      drawer: false,
      items: [{
        href: 'home',
        router: true,
        title: 'menu.home',
        icon: 'home'
      }, {
        href: 'elections',
        router: true,
        title: 'menu.elections',
        icon: 'extension'
      }, {
        href: 'about',
        router: true,
        title: 'menu.about',
        icon: 'domain'
      }],
      menu: false,
      languages: {
        en: 'English',
        de: 'Deutsch'
      }
    }
  },
  computed: {
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
    expertMode: {
      get () {
        return this.$store.state.expertMode
      },
      set (value) {
        this.$store.commit('expertMode', value)
      }
    }
  },
  methods: {
    changeLanguage (lang) {
      this.$root.$i18n.locale = lang
      this.$store.commit('language', lang)
    }
  }
}
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

<style>
  .tabs__wrapper{
    overflow: hidden !important;
  }
</style>
