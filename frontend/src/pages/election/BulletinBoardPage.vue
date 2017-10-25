<template>
    <v-container>

<div class="layout row wrap">
<div class="" style="float: left;font-size: 38px; color:#2196f3; width:60px"><i class="mdi icon mdi-bulletin-board" style="
    font-size: 48px; color: #2196f3; margin-top: 10px;"></i></div>
    <div style="color: #2196f3; clear: both;"><h3 class="my-3" style="color: #2196f3;">Bulletin Board</h3></div>
    </div>
    </div>

 <v-container grid-list-md text-xs-center>
    <v-layout row wrap>
     <v-flex xs12 md4>
       <v-card class="infoCard">
      <v-card-title primary-title>
        <div><span class="label grey--text">Unique Election Identifier
        <v-tooltip top>
                          <v-icon color="grey lighten-1" slot="activator">info</v-icon><span>Programmatic tooltip</span>
                       </v-tooltip></span>
        <div class="value">{{data.id}}</div>
        </div>
       </v-card-title>
       </v-card>
      </v-flex>

     <v-flex xs12 md4>
       <v-card class="infoCard">
      <v-card-title primary-title>
        <div><span class="label grey--text">Status
        <v-tooltip top>
                          <v-icon color="grey lighten-1" slot="activator">info</v-icon><span>Programmatic tooltip</span>
                       </v-tooltip></span>
        <div class="value">{{data.status}}</div>
        </div>
       </v-card-title>
       </v-card>
      </v-flex>


     <v-flex xs12 md4>
       <v-card class="infoCard">
      <v-card-title primary-title>
        <div><span class="label grey--text">Public Key
        <v-tooltip top>
                          <v-icon color="grey lighten-1" slot="activator">info</v-icon><span>Programmatic tooltip</span>
                       </v-tooltip></span>
        <div class="value"><BigIntLabel :mpzValue="data.publicKey"></BigIntLabel></div>
        </div>
       </v-card-title>
       </v-card>
      </v-flex>

     <v-flex xs12 md4>
       <v-card class="infoCard">
      <v-card-title primary-title>
        <div><span class="label grey--text">Candidates
        <v-tooltip top>
                          <v-icon color="grey lighten-1" slot="activator">info</v-icon><span>Programmatic tooltip</span>
                       </v-tooltip></span>
        <div class="value">{{data.candidates}}</div>
        </div>
       </v-card-title>
       </v-card>
      </v-flex>

     <v-flex xs12 md4>
       <v-card class="infoCard">
      <v-card-title primary-title>
        <div><span class="label grey--text">Counting Circles
        <v-tooltip top>
                          <v-icon color="grey lighten-1" slot="activator">info</v-icon><span>Programmatic tooltip</span>
                       </v-tooltip></span>
        <div class="value">{{data.countingCircles}}</div>
        </div>
       </v-card-title>
       </v-card>
      </v-flex>

     <v-flex xs12 md4>
       <v-card class="infoCard">
      <v-card-title primary-title>
        <div><span class="label grey--text">Selections
        <v-tooltip top>
                          <v-icon color="grey lighten-1" slot="activator">info</v-icon><span>Programmatic tooltip</span>
                       </v-tooltip></span>
        <div class="value">{{data.numberOfSelections}}</div>
        </div>
       </v-card-title>
       </v-card>
      </v-flex>

     <v-flex xs12 md4>
       <v-card class="infoCard">
      <v-card-title primary-title>
        <div><span class="label grey--text">Voters
        <v-tooltip top>
                          <v-icon color="grey lighten-1" slot="activator">info</v-icon><span>Programmatic tooltip</span>
                       </v-tooltip></span>
        <div class="value">{{data.voters}}</div>
        </div>
       </v-card-title>
       </v-card>
      </v-flex>


           <v-flex xs12 md4>
             <v-card class="infoCard">
            <v-card-title primary-title>
              <div><span class="label grey--text">Public Voting Credentials
              <v-tooltip top>
                                <v-icon color="grey lighten-1" slot="activator">info</v-icon><span>Programmatic tooltip</span>
                             </v-tooltip></span>
              <div class="value"> Voting Credentials for all voters</div>
              </div>
             </v-card-title>
 <v-card-actions style="height:33px; padding: 0px">

          <v-spacer></v-spacer>
          <v-btn icon @click.native="showCredentials = !showCredentials">
            <v-icon>{{ !showCredentials ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
          </v-btn>
        </v-card-actions>
        <v-slide-y-transition>
          <v-card-text v-show="showCredentials">
            <ul id="subList">
             <li v-for="(item, key, index) in data.publicVotingCredentials">
                {{ index}}
                 <ul>
                     X: <BigIntLabel :mpzValue="item[0]"></BigIntLabel>
                     Y: <BigIntLabel :mpzValue="item[1]"></BigIntLabel>
                 </ul>

             </li>
         </ul>
          </v-card-text>
        </v-slide-y-transition>
             </v-card>
            </v-flex>

      </v-flex>
      </v-layout>
      </v-container>
        <br>
    </v-container>
</template>

<script>
    export default {
        data: () => ({
          showCredentials: false
        }),
        computed: {
            data() {
                return {
                    id: this.$store.state.Election.electionID,
                    status: this.$store.getters.getStatusText,
                    publicKey: this.$store.state.BulletinBoard.publicKey,
                    voters: this.$store.state.BulletinBoard.voters,
                    candidates: this.$store.state.BulletinBoard.candidates,
                    publicVotingCredentials: this.$store.state.BulletinBoard.publicVotingCredentials,
                    numberOfSelections: this.$store.state.BulletinBoard.numberOfSelections,
                    countingCircles: this.$store.state.BulletinBoard.countingCircles,
                }
            }
        },
        created() {
            this.$socket.emit('join', {'election': this.$route.params["id"]});
        }
    };
</script>
