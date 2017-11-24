<template>
  <v-card>
    <v-card-title primary-title>
      <div class="headline">Voting Card</div>
    </v-card-title>
    <v-card-text>
      The Voting Card is secret and only the intended voter must be able to see the codes.
    </v-card-text>
    <v-list>
      <v-divider/>
      <v-list-tile :class="{ 'blue lighten-4': state == 0 }" title="Click to insert voting code" @click="insertVotingCode">
        <v-list-tile-title v-t="'voting_code'"></v-list-tile-title>
        <v-list-tile-sub-title>
          <confidentialityChip type="secret" />
        </v-list-tile-sub-title>
        <ScratchCard ref="votingCodeScratchCard">
          <div class="code">{{ card['votingCode'] }}</div>
        </ScratchCard>
      </v-list-tile>

      <v-divider/>

      <v-list-tile :class="{ 'blue lighten-4': state == 1 }" title="Click to insert confirmation code" @click="insertConfirmationCode">
        <v-list-tile-title v-t="'Voter.confirmation_code'"></v-list-tile-title>
        <v-list-tile-sub-title>
          <confidentialityChip type="secret" />
        </v-list-tile-sub-title>
        <ScratchCard ref="confirmationCodeScratchCard">
          <div class="code">{{ card['confirmationCode'] }}</div>
        </ScratchCard>
      </v-list-tile>

      <v-divider/>

      <v-divider/>

      <v-list-tile :class="{ 'blue lighten-4': state == 2 }" title="Make sure the finalization code on the left matches this code">
        <v-list-tile-title v-t="'Voter.finalization_code'"></v-list-tile-title>
        <v-list-tile-sub-title>
          <confidentialityChip type="public" />
        </v-list-tile-sub-title>
        <div class="code">{{ card['finalizationCode'] }}</div>
      </v-list-tile>
    </v-list>

      <!-- TODO card['verificationCodes'] should be a list of lists of verfication codes -->
      <v-layout v-for="(codes, codesIndex) in [card['verificationCodes']]" :class="{ 'blue lighten-4': state == 2 }" title="Make sure the verification on the left matches the corresponding code">
        <v-flex>
          <v-card flat>
            <v-card-text v-t="'Voter.verification_codes'"></v-card-text>
            <confidentialityChip type="public" />
          </v-card>
        </v-flex>
        <v-flex>
          <v-layout v-for="(code, i) in codes">
            <v-flex>{{ candidates[codesIndex][i].name }}</v-flex>
            <v-flex class="code">{{ code }}</v-flex>
          </v-layout>
        </v-flex>
      </v-layout>

  </v-card>
</template>

<script>
export default {
  props: {
    card: {
      type: Object,
      required: true
    },
    state: {
      type: Number,
      required: true
    },
    candidates: {
      type: Array,
      required: true
    },
    /*
    * Note: objects and arrays in JavaScript are passed by reference, so if the prop is an array
    * or object, mutating the object or array itself inside the child will affect parent state.
    * The property `code` is an object in order to set the codes in the parent.
    * Also see: https://vuejs.org/v2/guide/components.html#One-Way-Data-Flow
    */
    codes: {
      type: Object,
      required: false
    }
  },
  methods: {
    insertVotingCode () {
      if (this.$refs.votingCodeScratchCard.revealed && 'voting' in this.codes) {
        this.codes['voting'] = this.card['votingCode']
      }
    },
    insertConfirmationCode () {
      if (this.$refs.confirmationCodeScratchCard.revealed && 'confirmation' in this.codes) {
        this.codes['confirmation'] = this.card['confirmationCode']
      }
    }
  }
}
</script>

<style scoped>
.votingCard {
  user-select: none;
}
.code {
  margin: 5px 10px 5px 10px;
  font-family: monospace;
  white-space: nowrap;
}
</style>
