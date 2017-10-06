<template>
     <v-container>
        <h2>Ongoing election events</h2>
        <p>The following elections are still ongoing:</p>
        <v-list two-line subheader>
                <v-list-tile v-for="item in elections" v-bind:key="item.title" avatar @click="">
                   <v-list-tile-avatar>
                     <v-icon v-bind:class="[item.iconClass]">{{ item.icon }}</v-icon>
                   </v-list-tile-avatar>
                   <v-list-tile-content>
                     <v-list-tile-title>{{ item.title }}</v-list-tile-title>
                     <v-list-tile-sub-title>{{ item.subtitle }}</v-list-tile-sub-title>
                   </v-list-tile-content>
                   <v-list-tile-action>
                     <v-btn router icon ripple href="/#/election/1">
                       <v-icon class="grey--text text--lighten-1">info</v-icon>
                     </v-btn>
                   </v-list-tile-action>
                 </v-list-tile>
            </v-subheader>
        </v-list>
        <v-btn light to="newElection">
Create new</v-btn>

    </v-container>
</template>

<script>
  export default {
   data () {
       return {
          elections: [
                  { icon: 'assignment', iconClass: 'blue white--text', title: 'Präsidentenwahl FC Oberlupfigen', subtitle: 'Jan 20, 2018' },
                  { icon: 'call_to_action', iconClass: 'amber white--text', title: 'Abstimmung XY', subtitle: 'Jan 10, 2014' },
                ]
       }
     },

    mounted() {
    },
  };
</script>
