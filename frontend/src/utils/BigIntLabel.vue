<template>
  <p>
    {{ data.truncatedValue() }}
    <v-btn small flat icon v-popover="{ name: data.name }" style="margin-left: 0px">
      <v-icon>mdi-dots-horizontal</v-icon>
    </v-btn>
    <popover :name="data.name">
      <v-list>
        <v-list-tile-title class="datacardTitle" v-if="isString(mpzValue)">
          <b>{{ data.bitLength() }}-Bit number</b>
        </v-list-tile-title>
        <v-list-tile-title class="datacardValue">{{ mpzValue }}</v-list-tile-title>
      </v-list>
    </popover>
  </p>
</template>

<script>
export default {
  data: () => ({
    menu: false
  }),
  computed: {
    data () {
      return {
        truncatedValue: () => {
          // truncate the bigInt string
          if (this.mpzValue !== undefined && this.mpzValue !== null) {
            return this.mpzValue.toString().substring(0, 6)
          } else {
            return 'Invalid BigInt'
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
  props: {
    mpzValue: {
      type: String,
      required: true
    }
  },
  methods: {
    isString (s) {
      return typeof (s) === 'string' || s instanceof String
    }
  }
}
</script>

<style>
.vue-popover {
    width: 650px !important;
    padding: 15px;
}

p {
    display: inline;
}

.vue-popover .datacardTitle {
    text-transform: uppercase;
    font-size: 15px;
}

.vue-popover .datacardValue {
    overflow-wrap: break-word;
    word-wrap: break-word;
    white-space: pre-wrap;
    height: auto;
    font-size: 14px;
}
</style>
