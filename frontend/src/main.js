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
import BulletinBoardPage from './pages/election/BulletinBoardPage.vue'
import ElectionAuthorityPage from './pages/election/ElectionAuthorityPage.vue'
import Vuex from 'vuex'
import VueSocketio from 'vue-socket.io';
import {store} from './store/store.js'
import VueResource from 'vue-resource'
import BigIntLabel from './utils/BigIntLabel.vue';
import DataCard from './utils/DataCard.vue';
import NProgress from 'nprogress/nprogress.js';
import Toasted from 'vue-toasted';

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
        path: '/election/:id/admin',
        name: 'electionadmin',
        component: ElectionAdminPage,
    },
    {
        path: '/election/:id/printing',
        name: 'printingauth',
        component: PrintingAuthPage,
    },
    {
        path: '/election/:id/voter',
        name: 'voter',
        component: VoterPage,
    },
    {
        path: '/election/:id/bulletinBoard',
        name: 'bulletinboard',
        component: BulletinBoardPage,
    },
    {
        path: '/election/:id/electionAuthority',
        name: 'electionauthority',
        component: ElectionAuthorityPage,
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
Vue.use(Vuex);
Vue.use(VueResource);
Vue.component('BigIntLabel', BigIntLabel);
Vue.component('DataCard', DataCard);
Vue.use(Toasted, {position: 'top-right', duration: '4000'})

Vue.url.options.root = process.env.URL_ROOT;
Vue.use(VueSocketio, process.env.SOCKETIO_BASE_URL, store);

NProgress.configure({ showSpinner: false });


Vue.http.interceptors.push((request, next) => {
    NProgress.start();
    next((response) => {
        NProgress.done();
    });
});

new Vue({ // eslint-disable-line no-new
    el: '#app', store,
    router,
    render: h => h(App),
    components: {BigIntLabel},
});
