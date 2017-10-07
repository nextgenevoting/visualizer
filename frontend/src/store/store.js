import Vue from 'vue'
import Vuex from 'vuex'
import elections from './modules/elections'

Vue.use(Vuex)

export default new Vuex.Store({
    namespaced: true,
    state: {
        connected: false
    },
    mutations: {
        SOCKET_CONNECT: (state,  status) => {
            state.connected = true;
        },
        SOCKET_DISCONNECT: (state,  status) => {
            state.connected = false;
        },
        SOCKET_USERMESSAGE: (state,  message) => {
            console.log("SOCKET_USERMESSAGE called");
            state.message = message;
        }
    },
    actions: {
        /*socket_getdata: (context, message) => {
            // console.log(message.data);
            context.commit('updateData', message.data);
        }*/
    },
    modules: {
        elections
    },
})