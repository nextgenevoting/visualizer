import Vue from 'vue';
import Vuetify from 'vuetify';
import VueRouter from 'vue-router';
import App from './App.vue';
import HomePage from './pages/HomePage.vue';
import AboutPage from './pages/AboutPage.vue';
import ElectionsPage from './pages/ElectionsPage.vue';
import LoginPage from './pages/auth/LoginPage.vue';
import NewElectionPage from './pages/NewElectionPage.vue';
import ElectionOverviewPage from './pages/ElectionOverviewPage.vue'
import Vuex from 'vuex'
import storePlugin from './storePlugin'
import VueSocketio from 'vue-socket.io';
import { MyVuexStore } from './store.js'

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
});

Vue.use(Vuetify);
Vue.use(VueRouter);
Vue.use(Vuex)
Vue.use(storePlugin)
Vue.use(VueSocketio, 'http://localhost:5000', Vue.prototype.$dataStore);

new Vue({ // eslint-disable-line no-new
  el: '#app',
  router,
  render: h => h(App),
});
