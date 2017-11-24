<template>
  <span v-if="data.showConfidentiality" tabindex="0" class="ml-0 chip chip--label chip--small lighten-4" :class="colorClass">{{ type }}</span>
</template>

<script>
export default {
  props: {
    type: {
      type: String,
      required: true
    }
  },
  computed: {
    data () {
      return {
        showConfidentiality: this.$store.state.showConfidentiality
      }
    },
    colorClass () {
      var map = {
        'secret': 'red',
        'encrypted': 'yellow',
        'public': 'green'
      }

      return this.type in map ? map[this.type] : 'blue'
    }
  }
}
</script>
