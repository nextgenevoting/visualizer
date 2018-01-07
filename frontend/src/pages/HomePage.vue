<template>
  <v-container>
    <h2 class="my-3" v-t="'homePage.welcome.title'"></h2>
    <p v-t="'homePage.welcome.text'"></p>

    <v-btn flat blue :to="{ name: 'elections'}"><v-icon>mdi-arrow-right-bold-circle</v-icon> Start</v-btn>
  </v-container>
</template>
