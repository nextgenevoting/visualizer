<template>
  <p>{{ data.truncatedValue() }}<v-tooltip right>
   <v-icon slot="activator">mdi-dots-horizontal</v-icon>
    <span>{{ mpzValue }}</span>
    </v-tooltip></p>
</template>

<script>
    export default {
      computed: {
          data() {
            var self = this;
              return {
                  truncatedValue: function(){
                    if(self.mpzValue !== undefined && self.mpzValue !== null)
                        return self.mpzValue.toString().substring(0,10);
                    else
                        return "";
                    }
                  }
              }
      },
        props:{
            mpzValue: {
                type: String,
                required: true
            }
        },

        mounted() {
        },
    };
</script>

<style>
p{
    display: inline;
}
</style>