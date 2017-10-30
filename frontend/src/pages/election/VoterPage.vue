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


        <div v-if="status < 1">
            Before you can vote, the election must be set up
        </div>
        <div v-else>
            <v-flex xy12 md6 v-if="selectedVoter == null">
                Please choose a voter first<br><br>
                <v-btn @click="selectVoter">Select voter</v-btn>
            </v-flex>
            <v-flex xy12 md12 v-else>
                <v-stepper alt-labels :value="voter.status + 1">
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
                    <v-flex x12 md4>{{ votingCard }}</v-flex>
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
            status: {
              get: function(){
                return this.$store.state.Election.status;
              }
            },
            selectedVoter: {
                get: function(){
                    return this.$store.state.selectedVoter;
                }
            },
            voter: {
                get: function(id){
                    return this.$store.getters.getVoter(this.selectedVoter);
                }
            },
            votingCard: {
                get:function(){
                    if(this.selectedVoter != null && this.selectedVoter != 0){
                        return this.$store.getters.getVotingCard(this.selectedVoter);
                    }
                }
            }
        },
        created() {
            if(this.$store.getters.joinedElectionId !== this.$route.params['id'])
                this.$socket.emit('join', { election: this.$route.params['id'] });
        },
        methods: {
            generateVotingSheets: function (event) {
                this.$socket.emit('generateVotingSheets', {'election': this.$route.params["id"]});
            },
            selectVoter: function(){
                this.$store.commit("voterDialog", true);
            }

        },
        watch: {
            // whenever votingCard state changes, this function will be executed
            votingCard: function (newValue) {
               console.log(newValue);
            }
        },
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