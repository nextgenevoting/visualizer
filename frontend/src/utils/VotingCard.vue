<template>
  <v-card>
    <v-card-title primary-title>
      <div class="headline">Voting Card</div>
    </v-card-title>
    <v-card-text>
      {{$t('voting_card_text')}}
    </v-card-text>
    <v-list>
      <v-divider/>
      <v-list-tile :class="{ 'blue lighten-3': state === 0 }" :title="interactive && votingCodeRevealed ? 'Click to insert voting code' : ''">
        <v-list-tile-title v-t="'voting_code'"></v-list-tile-title>
        <v-list-tile-sub-title>
          <confidentialityChip type="secret" />
        </v-list-tile-sub-title>
        <ScratchCard :scratchable="this.scratchable" ref="votingCodeScratchCard" :revealed="votingCodeRevealed" @revealed="revealCode(0)">
          <div class="code" :class="{ 'pointer': interactive && votingCodeRevealed }" @click="insertVotingCode">{{ card['votingCode'] }}</div>
        </ScratchCard>
      </v-list-tile>

      <v-divider/>

      <v-list-tile :class="{ 'blue lighten-3': state === 1  }" :title="interactive && confirmationCodeRevealed ? 'Click to insert confirmation code' : ''">
        <v-list-tile-title v-t="'Voter.confirmation_code'"></v-list-tile-title>
        <v-list-tile-sub-title>
          <confidentialityChip type="secret" />
        </v-list-tile-sub-title>
        <ScratchCard :scratchable="this.scratchable" ref="confirmationCodeScratchCard" :revealed="confirmationCodeRevealed" @revealed="revealCode(1)">
          <div class="code" :class="{ 'pointer': interactive && confirmationCodeRevealed }" @click="insertConfirmationCode">{{ card['confirmationCode'] }}</div>
        </ScratchCard>
      </v-list-tile>

      <v-divider/>

      <v-list-tile :class="{ 'blue lighten-3': state === 2 }" :title="interactive ? 'Make sure the finalization code on the left matches this code' : ''">
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
            <v-list-tile-title class="code_title">{{ candidate.name }}</v-list-tile-title>
            <div class="code">{{ candidate.verificationCode }}</div>
          </v-list-tile>
        </v-list>
      </v-flex>
    </div>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'

export default {
  props: {
    card: {
      type: Object,
      required: true
    },
    scratchable: {
      type: Boolean,
      required: true,
      default: true
    },
    interactive: {
      type: Boolean,
      required: true,
      default: false
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
    ...mapState({
      selectedVoter: state => state.selectedVoter
    }),
    voter: {
      get: function () {
        return this.$store.getters.getVoter(this.selectedVoter)
      }
    },
    votingCodeRevealed () {
      if (this.interactive === false) { return false }
      return this.voter.votingCodeRevealed
    },
    confirmationCodeRevealed () {
      if (this.interactive === false) { return false }
      return this.voter.confirmationCodeRevealed
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
      if (this.votingCodeRevealed) {
        this.codes['voting'] = this.card['votingCode']
      }
    },
    insertConfirmationCode () {
      if (this.confirmationCodeRevealed) {
        this.codes['confirmation'] = this.card['confirmationCode']
      }
    },
    revealCode (codeIndex) {
      this.$http.post('revealCode',
        {
          'election': this.$route.params['electionId'],
          'voterId': this.$route.params['voterId'],
          'codeIndex': codeIndex

        }
      ).then(response => {
        response.json().then((data) => {
        })
      }).catch(e => {
        this.$toasted.error(e.body.message)
      })
    }

  }
}
</script>

<style scoped>
.code {
  margin: 5px 10px 5px 10px;
  font-family: monospace;
  white-space: nowrap;
  font-size: 16px;
  user-select: none;
}
.code_title {
  font-size: 16px;
}
.pointer {
  cursor: pointer;
}
</style>
