<template>
  <div class="layout row wrap">
    <v-flex xy6 md6>
      <div class="content-header">
        <v-icon>{{ icon }}</v-icon>
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
      required: true,
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
  font-size: 38px;
  color: #505050;
  width: 60px;
}

.layout {
}

.content-header .icon {
  margin-top: 18px;
  font-size: 36px;
  color: #505050 !important;
}

.right {
  margin-top: 18px;
  text-align: right;
}

.my-3 {
  color: #505050;
  font-size: 32px;
}
</style>
