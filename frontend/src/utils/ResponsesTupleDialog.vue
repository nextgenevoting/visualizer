<template>
  <v-dialog v-model="visible" width="800px" @close="this.$emit('close')">
    <v-card>
      <v-card-title>
        <span class="headline" v-if="popupTitle !== undefined">{{ popupTitle }}</span>
        <span class="headline" v-else>{{$t('tuple_with_n_elements', {n: tuple.length }) }}</span>
      </v-card-title>
      <v-card-text>
        {{$t('value_of')}} <b>b</b>: (<span v-for="(tpl, index) in tuple[0]" :key="index">
          <BigIntLabel :mpzValue="tpl" /><span v-if="index < tuple[0].length - 1">, </span>
        </span>)
      </v-card-text>
      <v-card-text>
        {{$t('value_of')}} <b>C</b>:  <div v-for="(list, index) in tuple[1]" :key="index">
          (<span v-for="(tpl, i) in list">
            <span v-if="tpl === null">NULL</span><ByteArrayLabel v-else :value="tpl" /><span v-if="i < list.length - 1">, </span>
          </span>)
        </div>
      </v-card-text>
      <v-card-text>
        {{$t('value_of')}} <b>d</b>:
        <BigIntLabel :mpzValue="tuple[2]" />
      </v-card-text>
<!--
      <v-card-text>
<pre>
{{ JSON.stringify(tuple, null, 2) }}
</pre>
      </v-card-text>
-->
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    visible: {
      type: Boolean,
      required: true,
      default: false
    },
    tuple: {
      type: Array,
      required: true
    },
    popupTitle: {
      type: String,
      requried: false
    },
    icon: {
      type: String,
      requried: false
    }
  },
  data: () => ({
  }),
  computed: {
    data () {
      return {
        truncatedValue: () => {
          if (this.tuple !== undefined && this.tuple !== null) {
            return this.tupleValue.toString().substring(0, 10)
          } else {
            return ''
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
    clickButton: function (event) {
      this.dialog = !this.dialog
    }
  },
  watch: {
    visible: function (value) {
      if (value === false) {
        this.$emit('close')
      }
    }
  }
}
</script>
