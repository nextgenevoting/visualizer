<template>
  <div class="layout row wrap">
    <v-flex xy6 md6>
      <div class="content-header">
        <v-icon v-if="icon">{{ icon }}</v-icon>
        <span v-if="customicon" style="">
          <i  :class="customicon" style="font-size:7px"></i>
        </span>
      </div>
      <h3 class="my-3">{{ title }}</h3>
    </v-flex>
    <v-flex xy6 md6 class="right">
      <slot></slot>
    </v-flex>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true,
      default: 'NoTitle'
    },
    icon: {
      type: String,
      required: false,
      default: ''
    },
    customicon: {
      type: String,
      required: false,
      default: ''
    }
  },
  mounted () {
  }
}
</script>

<style scoped>
.content-header {
  float: left;
  font-size: 24px;
  color: #505050;
  width: 45px;
  line-height: 1.4em;
  margin-left: 10px;
}

.layout {
}

.content-header .icon {
  margin-top: 14px !important;
  font-size: 32px !important;
  color: #505050 !important;
}

.right {
  margin-top: 18px;
  text-align: right;
}

.my-3 {
  margin-top: 12px !important;
  margin-bottom: 16px !important;
  font-size:24px;
}
</style>
