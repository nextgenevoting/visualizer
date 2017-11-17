import Vue from 'vue'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import VueRouter from 'vue-router'
import VueI18n from 'vue-i18n'
import VueI18nDirectives from 'vue-i18n-directives'
import VueResource from 'vue-resource'
import VueSocketio from 'vue-socket.io'
import NProgress from 'nprogress/nprogress.js'
import { store } from './store/store.js'
import App from './App.vue'
import HomePage from './pages/HomePage.vue'
import AboutPage from './pages/AboutPage.vue'
import ElectionsPage from './pages/ElectionsPage.vue'
import LoginPage from './pages/auth/LoginPage.vue'
import NewElectionPage from './pages/NewElectionPage.vue'
import VoterPage from './pages/election/VoterPage.vue'
import PrintingAuthPage from './pages/election/PrintingAuthPage.vue'
import ElectionOverviewPage from './pages/election/ElectionOverviewPage.vue'
import ElectionAdminPage from './pages/election/ElectionAdminPage.vue'
import BulletinBoardPage from './pages/election/BulletinBoardPage.vue'
import ElectionAuthorityPage from './pages/election/ElectionAuthorityPage.vue'
import ConfirmationTaskPage from './pages/election/electionAuthoritySubpages/ConfirmationTaskPage.vue'
import CheckBallotTaskPage from './pages/election/electionAuthoritySubpages/CheckBallotTaskPage.vue'
import MixingPage from './pages/election/electionAuthoritySubpages/MixingPage.vue'
import DecryptionPage from './pages/election/electionAuthoritySubpages/DecryptionPage.vue'
import SelectVoterDialog from './utils/SelectVoterDialog.vue'
import LoadingOverlay from './utils/LoadingOverlay.vue'
import BallotList from './utils/BallotList.vue'
import BigIntLabel from './utils/BigIntLabel.vue'
import TupleLabel from './utils/TupleLabel.vue'
import DataCard from './utils/DataCard.vue'
import ContentTitle from './utils/ContentTitle.vue'
import Toasted from 'vue-toasted'
import Raphael from 'raphael/raphael'
import { DonutChart } from 'vue-morris'
import Popover from 'vue-js-popover'
import lodash from 'lodash'
import VueLodash from 'vue-lodash'
global.Raphael = Raphael

const routes = [
  { path: '/home', name: 'home', component: HomePage },
  { path: '/about', name: 'about', component: AboutPage },
  { path: '/elections', name: 'elections', component: ElectionsPage },
  { path: '/newelection', name: 'newelection', component: NewElectionPage },
  { path: '/election/:electionId', name: 'electionoverview', component: ElectionOverviewPage },
  { path: '/election/:electionId/admin', name: 'electionadmin', component: ElectionAdminPage },
  { path: '/election/:electionId/printing', name: 'printingauth', component: PrintingAuthPage },
  { path: '/election/:electionId/voter', name: 'voter', component: VoterPage },
  { path: '/election/:electionId/bulletinBoard', name: 'bulletinboard', component: BulletinBoardPage },
  { path: '/election/:electionId/electionAuthority/:authid', name: 'electionauthority', component: ElectionAuthorityPage },
  { path: '/login', name: '/login', component: LoginPage },
  { path: '*', redirect: { name: 'home' } }
]

const router = new VueRouter({
  routes,
  root: '/home',
  mode: 'history'
})

Vue.use(VueLodash, lodash)
Vue.use(Vuetify)
Vue.use(VueRouter)
Vue.use(Vuex)
Vue.use(VueResource)
Vue.use(VueI18n)
Vue.use(VueI18nDirectives)
Vue.use(Popover)
Vue.use(Toasted, { position: 'top-right', duration: '4000' })

Vue.component('BigIntLabel', BigIntLabel)
Vue.component('TupleLabel', TupleLabel)
Vue.component('DataCard', DataCard)
Vue.component('LoadingOverlay', LoadingOverlay)
Vue.component('ContentTitle', ContentTitle)
Vue.component('SelectVoterDialog', SelectVoterDialog)
Vue.component('ConfirmationTaskPage', ConfirmationTaskPage)
Vue.component('CheckBallotTaskPage', CheckBallotTaskPage)
Vue.component('MixingPage', MixingPage)
Vue.component('DecryptionPage', DecryptionPage)
Vue.component('DonutChart', DonutChart)
Vue.component('BallotList', BallotList)

Vue.url.options.root = process.env.URL_ROOT
Vue.use(VueSocketio, process.env.SOCKETIO_BASE_URL, store)

NProgress.configure({ showSpinner: false })

Vue.http.interceptors.push((request, next) => {
  NProgress.start()
  next((response) => {
    NProgress.done()
  })
})

const translations = require('./translations.yaml')
const languages = [ 'en', 'de' ] // the first language in the list is considered the primary language

const i18n = new VueI18n({
  locale: store.state.language,
  fallbackLocale: languages[0],
  messages: Object.assign(...languages.map((lang) => {
    return { [lang]: (function flatten (obj, lang) {
      if (Object.keys(obj).every((key) => obj[key].constructor === String)) {
        return lang in obj ? obj[lang] : undefined
      } else {
        return Object.assign(...Object.keys(obj).map((key) => ({ [key]: flatten(obj[key], lang) })))
      }
    })(translations, lang)}
  }))
})

new Vue({ // eslint-disable-line no-new
  el: '#app',
  store,
  router,
  i18n,
  render: h => h(App),
  components: { BigIntLabel }
})
