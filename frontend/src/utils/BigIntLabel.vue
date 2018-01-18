<template>
  <span>
    {{ data.truncatedValue() }}
    <v-menu offset-y :max-width="600">
      <v-btn small flat icon slot="activator" style="margin-left: 0px; color: rgba(0,0,0,.54)" v-if="this.hasValue()">
        <v-icon>mdi-dots-horizontal</v-icon>
      </v-btn>
      <v-card>
        <v-card-title v-if="isString(mpzValue)" class="subheading" style="padding-bottom: 0px;">
          {{ data.bitLength() }}-Bit {{$t('main.number')}}
        </v-card-title>
        <v-card-text>
          <div class="wrap">{{ mpzValue }}</div>
        </v-card-text>
      </v-card>
    </v-menu>
  </span>
</template>

<script>
export default {
  props: {
    mpzValue: {
      type: String,
      required: true
    }
  },
  computed: {
    data () {
      return {
        truncatedValue: () => {
          // truncate the bigInt string
          if (this.hasValue()) {
            return this.mpzValue.toString().substring(0, 6)
          } else {
            return ''
          }
        },
        bitLength: () => {
          // Calculating the exact bitlength only works up to ~1024 bit; numbers larger than that will simply be "infinity"
          // Math.ceil(Math.log(bigIntString) / Math.log(2))
          // alternative: Use an estimate, or use a bigint library
          const expectedBitLengths = [160, 224, 256, 1024, 2048, 3072]
          let estimate = Math.round(this.mpzValue.length * Math.log2(10))
          // check if the estimated bitlength is in +- 10 range of an expected bitlength
          for (let e of expectedBitLengths) {
            if (estimate >= e - 10 && estimate <= e + 10) {
              return e
            }
          }
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
    },
    hasValue () {
      return this.mpzValue !== undefined && this.mpzValue !== null
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
