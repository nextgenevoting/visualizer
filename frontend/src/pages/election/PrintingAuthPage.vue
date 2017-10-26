<template>
    <v-container>
        <div class="layout row wrap">
            <div class="contentHeader">
                <i class="mdi icon mdi-printer"></i>
            </div>
            <h3 class="my-3">Printing Authority</h3>
        </div>
        <br>
        <div v-if="data.status == 0">
            Before voting cards can be printed, the election administrator must set up the election.
        </div>

        <div v-if="data.status == 1">
            <v-btn color="primary" v-on:click="printVotingCards">Print voting cards</v-btn>
        </div>

        <div v-if="data.status == 2">
            Voting cards: {{ data.votingCards }}
            <br>
            <v-btn color="primary" v-on:click="sendVotingCards">Send voting cards to voters</v-btn>

        </div>
        <div v-if="data.status == 3">
            Voting cards have been delivered to the voters! <br><br>
            Voting Sheets: {{ data.votingCards }}
        </div>
    </v-container>
</template>

<script>
    export default {
    computed: {
        data() {
          return {
            voters: this.$store.state.BulletinBoard.voters,
            status: this.$store.state.Election.status,
            votingCards: this.$store.state.PrintingAuthority.votingCards
          }
        }
    },
    created() {
        this.$socket.emit('join', {'election': this.$route.params["id"]});
    },
    methods: {
        printVotingCards: function (event) {
          this.$http.post('printVotingCards', {
            'election': this.$route.params["id"],
          }
          ).then(response => {response.json().then((data) => {
            // success callback
          });
          }, response => {
            // error callback
          });
        },
        sendVotingCards: function (event) {
            this.$http.post('sendVotingCards', {
                    'election': this.$route.params["id"],
                }
            ).then(response => {response.json().then((data) => {
                // success callback
            });
            }, response => {
                // error callback
            });
        },
      }
    };
</script>
