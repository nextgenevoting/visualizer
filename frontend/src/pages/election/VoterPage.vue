<template>
    <v-container grid-list-md>
        <div class="layout row wrap">
            <div class="contentHeader">
                <i class="mdi icon mdi-account"></i>
            </div>
            <h3 class="my-3">
                <p>Voters</p>
            </h3>
        </div>


        <div v-if="data.status < 2">
            Before you can vote, the election must be set up and voting cards printed
        </div>
        <div v-else>
            <v-flex xy12 md6 v-if="data.selectedVoter == null" class="text-xs-center">

                <v-card class="text-xs-center">
                    <v-card-title primary-title class="primaryContent">
                        <div><span class="label grey--text">Please choose a voter</span></div>
                    </v-card-title>
                    <v-btn @click="selectVoter">Choose voter</v-btn>
                </v-card>
            </v-flex>
            <v-flex xy12 md12 v-else>
                <v-stepper alt-labels :value="data.getVoter().status + 1">
                    <v-stepper-header>
                        <v-stepper-step step="1">Vote Casting</v-stepper-step>
                        <v-divider></v-divider>
                        <v-stepper-step step="2">Confirmation</v-stepper-step>
                        <v-divider></v-divider>
                        <v-stepper-step step="3">Finalization</v-stepper-step>
                    </v-stepper-header>
                </v-stepper>
                <div class="layout row wrap">
                    <v-flex x12 md8>Selection form...</v-flex>
                    <v-flex x12 md4>{{ data.getVotingCard() }}</v-flex>
                </div>
            </v-flex>
        </div>

    </v-container>
</template>

<script>
    export default {
        data: () => ({
        }),
        computed: {
            data() {
                var self = this;
                return {
                    status: this.$store.state.Election.status,
                    voters: this.$store.state.Voter.voters,
                    selectedVoter: this.$store.state.selectedVoter,
                    getVoter: function(voterID){
                        return self.$store.getters.getVoter(self.data.selectedVoter);
                    },
                    getVotingCard: function(voterID){
                        return self.$store.getters.getVotingCard(self.data.selectedVoter);
                    }
                }
            }
        },
        created() {
            this.$socket.emit('join', {'election': this.$route.params["id"]});
            this.unsub = this.$store.subscribe((mutation, state) => console.log(mutation));
        },
        beforeDestroy() {
            console.log("before destroy");
            this.unsub();
        },
        methods: {
            generateVotingSheets: function (event) {
                this.$socket.emit('generateVotingSheets', {'election': this.$route.params["id"]});
            },
            selectVoter: function(){
                this.$store.commit("voterDialog", true);
            }

        }
    };
</script>
<style>
    .application--light .stepper {
        background: transparent !important;
    }

    .stepper {
        box-shadow: none !important
    }

</style>