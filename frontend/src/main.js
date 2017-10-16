import Vue from 'vue';
import Vuetify from 'vuetify';
import VueRouter from 'vue-router';
import App from './App.vue';
import HomePage from './pages/HomePage.vue';
import AboutPage from './pages/AboutPage.vue';
import ElectionsPage from './pages/ElectionsPage.vue';
import LoginPage from './pages/auth/LoginPage.vue';
import NewElectionPage from './pages/NewElectionPage.vue';
import VoterPage from './pages/election/VoterPage.vue';
import PrintingAuthPage from './pages/election/PrintingAuthPage.vue';
import ElectionOverviewPage from './pages/election/ElectionOverviewPage.vue'
import ElectionAdminPage from './pages/election/ElectionAdminPage.vue'
import Vuex from 'vuex'
import storePlugin from './store/storeplugin'
import VueSocketio from 'vue-socket.io';
import { MyVuexStore } from './store/store.js'
import VueResource from 'vue-resource'

const routes = [
  {
    path: '/home',
    name: 'home',
    component: HomePage,
  },
  {
    path: '/about',
    name: 'about',
    component: AboutPage,
  },
  {
    path: '/elections',
    name: 'elections',
    component: ElectionsPage,
  },
  {
    path: '/newelection',
    name: 'newelection',
    component: NewElectionPage,
  },
  {
    path: '/election/:id',
    name: 'electionoverview',
    component: ElectionOverviewPage,
  },
  {
    path: '/election/admin/:id',
    name: 'electionadmin',
    component: ElectionAdminPage,
  },
  {
    path: '/election/print/:id',
    name: 'printingauth',
    component: PrintingAuthPage,
  },
  {
      path: '/election/voter/:id',
      name: 'voter',
      component: VoterPage,
  },
  {
    path: '/login',
    name: '/login',
    component: LoginPage,
  },
  {
    path: '*',
    redirect: {
      name: 'home',
    },
  },
];
const router = new VueRouter({
  routes,
  root: '/home',
  mode: 'history'
});

Vue.use(Vuetify);
Vue.use(VueRouter);
Vue.use(Vuex)
Vue.use(VueResource)
Vue.use(storePlugin)

if (process.env.SOCKETIO_BASE_URL !== undefined) {
  Vue.url.options.root = process.env.SOCKETIO_BASE_URL;
} else {
  Vue.url.options.root = 'http://localhost:5000';
}

Vue.use(VueSocketio, Vue.url.options.root, Vue.prototype.$dataStore);

new Vue({ // eslint-disable-line no-new
  el: '#app',
  router,
  render: h => h(App),
});
