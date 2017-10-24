import Vue from 'vue'
import Vuex from 'vuex'
import Election from './modules/Election'
import BulletinBoard from './modules/BulletinBoard'
import PrintingAuthority from './modules/PrintingAuthority'
import Voter from './modules/Voter'


Vue.use(Vuex)

export const store = new Vuex.Store({
    namespaced: false,
    state: {
        connected: false,
    },
    mutations: {
        SOCKET_CONNECT: (state,  status) => {
            state.connected = true;
            // router.push({name: 'elections'});
        },
        SOCKET_DISCONNECT: (state,  status) => {
            state.connected = false;
        }
    },
    actions: {
        /*socket_getdata: (context, message) => {
            // console.log(message.data);
            context.commit('updateData', message.data);
        }*/
    },
    modules: {
        Election,
        BulletinBoard,
        PrintingAuthority,
        Voter
    },
})