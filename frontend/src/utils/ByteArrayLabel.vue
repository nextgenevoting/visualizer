<template>
  <span>
    {{ data.truncatedValue() }}
    <v-menu offset-y :max-width="600">
      <v-btn small flat icon slot="activator" style="margin-left: 0px; color: rgba(0,0,0,.54)">
        <v-icon>mdi-dots-horizontal</v-icon>
      </v-btn>
      <v-card>
        <v-card-title v-if="isString(value) && title != null" class="subheading" style="padding-bottom: 0px;">
          {{ this.title}}
        </v-card-title>
        <v-card-title v-else class="subheading" style="padding-bottom: 0px;">
          {{ $t('array_of_n', {n : data.byteLength()})}}
        </v-card-title>



        <v-card-text>
          <div class="wrap">{{ value }}</div>
        </v-card-text>
      </v-card>
    </v-menu>
  </span>
</template>

<script>
export default {
  props: {
    value: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: false
    }
  },
  computed: {
    data () {
      return {
        truncatedValue: () => {
          if (this.value !== undefined && this.value !== null) {
            return this.value.toString().substring(0, 6)
          } else {
            return 'Invalid byte array'
          }
        },
        byteLength: () => {
          return this.value.length
        },
        name: (function () {
          return String(Math.random())
        }())
      }
    }
  },
  methods: {
    isString (s) {
      return typeof (s) === 'string' || s instanceof String
    }
  }
}
</script>

<style scoped>
.wrap {
  overflow-wrap: break-word;
  word-wrap: break-word;
  white-space: pre-wrap;
}
</style>
