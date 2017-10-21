<template>
  <p>{{ data.truncatedValue }}<v-tooltip right>
   <v-icon slot="activator">mdi-dots-horizontal</v-icon>
    <span>{{ mpzValue }}</span>
    </v-tooltip></p>
</template>

<script>
    export default {
      computed: {
          data() {
              return {
                  truncatedValue: this.mpzValue.substring(0,10)
              }
          },
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