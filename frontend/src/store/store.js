import Vue from 'vue'
import Vuex from 'vuex'
import election from './modules/election'


Vue.use(Vuex)

export default new Vuex.Store({
    namespaced: false,
    state: {
        connected: false,
        elections: []
    },
    mutations: {
        SOCKET_CONNECT: (state,  status) => {
            state.connected = true;
        },
        SOCKET_DISCONNECT: (state,  status) => {
            state.connected = false;
            location.href("/elections");
        },
        SOCKET_SYNCELECTIONS: (state, data) => {
            state.elections = JSON.parse(data)
        }
    },
    actions: {
        /*socket_getdata: (context, message) => {
            // console.log(message.data);
            context.commit('updateData', message.data);
        }*/
    },
    modules: {
        election
    },
})