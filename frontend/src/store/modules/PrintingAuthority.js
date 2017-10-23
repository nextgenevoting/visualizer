// initial state
const state = {
    votingCards: [],
}

// mutations
const mutations = {
    SOCKET_SYNCPRINTINGAUTHORITY: (state, data) => {
        console.log("SOCKET_SYNCPRINTINGAUTHORITY called");

        var printingAuthorityState = JSON.parse(data.printingAuthorityState);
        console.log(printingAuthorityState);
        state.votingCards = printingAuthorityState.votingCards;
    }
}

export default {
    state,
    mutations
}