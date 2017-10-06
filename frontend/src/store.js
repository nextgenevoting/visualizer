import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        count: 1,
        message : "None",
        connected: false,
        elections: []
    },
    mutations: {
        SOCKET_CONNECT: (state,  status) => {
            state.connected = true;
        },
        SOCKET_DISCONNECT: (state,  status) => {
            state.connected = false;
        },
        SOCKET_USERMESSAGE: (state,  message) => {
            state.message = message;
        },
        SOCKET_GETUPDATE: (state, data) => {
            state.message = data.data.message;
            state.count = data.data.counter;
        },
        SOCKET_GETELECTIONS: (state, data) => {
            state.elections = data.elections
        }
    },
    actions: {
        /*socket_getdata: (context, message) => {
            // console.log(message.data);
            context.commit('updateData', message.data);
        }*/
    }
})