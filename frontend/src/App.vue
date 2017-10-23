<template>
    <v-app id="app">
        <v-navigation-drawer temporary v-model="drawer">
            <v-list>
                <v-list-tile>
                    <v-list-tile-content>
                        <v-list-tile-title >
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
                <v-toolbar-title><img src="public/logo.png" style="height:22px"></v-toolbar-title>
                <v-spacer></v-spacer>
                <v-btn icon>
                    <v-icon>mdi-translate</v-icon>
                </v-btn>
                <v-btn icon @click.native.stop="openGithub()">
                    <v-icon>home</v-icon>
                </v-btn>
            </v-toolbar>
             <v-tabs dark fixed icons centered>
                 <v-tabs-bar class="blue" v-show="$route.path.includes('/election/') ? true : false">
                  <v-tabs-slider color="yellow"></v-tabs-slider>
                   <v-tabs-item ripple :to="{ name: 'electionoverview', params: {id: $route.params['id'] }}">
                    <v-icon>mdi-view-dashboard</v-icon>
                    Overview
                  </v-tabs-item>
                  <v-tabs-item ripple :to="{ name: 'electionadmin', params: {id: $route.params['id'] }}">
                     <v-badge color="">
                        <v-icon slot="badge" dark v-if="status == 0">notifications</v-icon>
                       <v-icon>mdi-account-key</v-icon>
                       </v-badge>
                      Election Admin
                  </v-tabs-item>
                  <v-tabs-item ripple :to="{ name: 'printingauth', params: {id: $route.params['id'] }}">
                      <v-badge color="">
                       <v-icon slot="badge" dark v-if="status == 1">notifications</v-icon>
                      <v-icon>mdi-printer</v-icon>
                      </v-badge>
                      Printing Auth.
                </v-tabs-item>
                     <v-tabs-item ripple :to="{ name: 'voter', params: {id: $route.params['id'] }}">
                    <v-icon>mdi-account</v-icon>
                    Voter
                  </v-tabs-item>
                     <v-tabs-item ripple :to="{ name: 'bulletinboard', params: {id: $route.params['id'] }}">
                        <v-icon>mdi-checkbox-marked-outline</v-icon>
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

        <v-snackbar success top :timeout="2000" v-model="onlineNotification">
            Websocket connection established!
            <v-btn dark flat @click.native="onlineNotification = false">Close</v-btn>
        </v-snackbar>

    </v-app>
</template>

<script type="text/babel">
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
      };
    },
    computed:{

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
               return this.$store.state.BulletinBoard.status
            },
          set (value) {
          }
       },
    },
    methods: {
      openGithub() {
        window.open('https://github.com/disjfa/vuetify-sidebar-template');
      },
    }
  };
</script>

<style lang="stylus">
@import '../node_modules/vuetify/src/stylus/main';
@import 'css/main.css';
</style>
