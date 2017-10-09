 <template>
<v-container grid-list-xl text-xs-center>
    <v-layout row wrap>
      <v-flex xs10 offset-xs1>
        <v-card class="pa-5">
           <span class="headline">Create new election</span>
           <v-form>
              <v-text-field
                label="Title"
                v-model="title"
                required
              ></v-text-field>

              <v-btn @click="createElection" class="">Create</v-btn>
            </v-form>
        </v-card>
      </v-flex>
    </v-layout>
 </v-container>
</template>

<script>
    export default {
    data: function(){
        return {
            title: ''
        }
    },
      methods: {
        createElection: function(){
          this.$socket.emit('createelection', { title: this.title});
        }
      }
    };
</script>

