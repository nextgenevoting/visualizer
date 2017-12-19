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
      <v-list-tile :class="{ 'blue lighten-3': active && state === 0 }" :title="active ? 'Click to insert voting code' : ''">
        <v-list-tile-title v-t="'voting_code'"></v-list-tile-title>
        <v-list-tile-sub-title>
          <confidentialityChip type="secret" />
        </v-list-tile-sub-title>
        <ScratchCard :scratchable="active" ref="votingCodeScratchCard">
          <div class="code" :class="{ 'pointer': active }" @click="insertVotingCode">{{ card['votingCode'] }}</div>
        </ScratchCard>
      </v-list-tile>

      <v-divider/>

      <v-list-tile :class="{ 'blue lighten-3': active && state === 1 }" :title="active ? 'Click to insert confirmation code' : ''">
        <v-list-tile-title v-t="'Voter.confirmation_code'"></v-list-tile-title>
        <v-list-tile-sub-title>
          <confidentialityChip type="secret" />
        </v-list-tile-sub-title>
        <ScratchCard :scratchable="active" ref="confirmationCodeScratchCard">
          <div class="code" :class="{ 'pointer': active }" @click="insertConfirmationCode">{{ card['confirmationCode'] }}</div>
        </ScratchCard>
      </v-list-tile>

      <v-divider/>

      <v-list-tile :class="{ 'blue lighten-3': active && state === 2 }" :title="active ? 'Make sure the finalization code on the left matches this code' : ''">
        <v-list-tile-title v-t="'Voter.finalization_code'"></v-list-tile-title>
        <v-list-tile-sub-title>
          <confidentialityChip type="public" />
        </v-list-tile-sub-title>
        <div class="code">{{ card['finalizationCode'] }}</div>
      </v-list-tile>

      <v-divider/>
    </v-list>

    <div v-for="(candidates, index) in candidateVerificationCodes">
      <v-divider v-if="index > 0" />
      <v-toolbar flat dense>
        <v-list>
          <v-list-tile>
            <v-list-tile-title class="title">
              {{ $t('Voter.verification_codes_election_n', { n: index + 1 }) }}
              <confidentialityChip type="public" />
            </v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-toolbar>
      <v-flex title="Make sure the verification on the left matches the corresponding code">
        <v-list dense>
          <v-list-tile v-for="candidate in candidates" :key="candidate.index">
            <v-list-tile-title>{{ candidate.name }}</v-list-tile-title>
            <div class="code">{{ candidate.verificationCode }}</div>
          </v-list-tile>
        </v-list>
      </v-flex>
    </div>
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
      required: false,
      default: undefined
    }
  },
  computed: {
    active () {
      return this.codes !== undefined
    },
    candidateVerificationCodes () {
      var list = []
      var i = 0
      this.candidates.forEach((candidates) => {
        candidates.forEach((candidate) => {
          candidate.verificationCode = this.card['verificationCodes'][i++]
        })
        list.push(candidates)
      })
      return list
    }
  },
  methods: {
    insertVotingCode () {
      if (this.active && this.$refs.votingCodeScratchCard.revealed && 'voting' in this.codes) {
        this.codes['voting'] = this.card['votingCode']
      }
    },
    insertConfirmationCode () {
      if (this.active && this.$refs.confirmationCodeScratchCard.revealed && 'confirmation' in this.codes) {
        this.codes['confirmation'] = this.card['confirmationCode']
      }
    }
  }
}
</script>

<style scoped>
.code {
  margin: 5px 10px 5px 10px;
  font-family: monospace;
  white-space: nowrap;
  user-select: none;
}
.pointer {
  cursor: pointer;
}
</style>
