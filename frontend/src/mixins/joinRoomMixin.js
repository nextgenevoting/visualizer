export default {
    created() {
        if (this.$store.getters.joinedElectionId !== this.$route.params['id'])
            this.$socket.emit('join', {election: this.$route.params['id']});
    },
    methods: {

    }
}