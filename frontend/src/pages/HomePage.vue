<template>
  <v-container fluid class="pa-0">
    <v-container>
      <h2 v-t="'welcome.title'"></h2>
      <p v-t="'welcome.text'"></p>
    </v-container>
  </v-container>
</template>

<i18n>
en:
  welcome:
    title: Welcome
    text: Welcome to the CHVote demonstrator
de:
  welcome:
    title: Willkommen
    text: Willkommen beim CHVote-Demonstrator
</i18n>

<script>
export default {
  data () {
    return { }
  }
}
</script>
