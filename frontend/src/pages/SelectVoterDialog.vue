<template>
<v-dialog v-model="showDialog" max-width="400px">
    <v-card>
        <v-card-title>
            Choose voter for vote casting
        </v-card-title>
        <v-card-text>
            <v-list>
                <v-list-tile v-for="(item, index) in this.$store.state.Voter.voters" v-bind:key="item.name"
                             active-class="default-class your-class"
                             @click="selectVoter(item.id)">
                    <v-list-tile-avatar>
                        <v-icon>mdi-account</v-icon>
                    </v-list-tile-avatar>
                    <v-list-tile-content>
                        <v-list-tile-title>{{ item.name }}</v-list-tile-title>
                    </v-list-tile-content>
                    <v-list-tile-action>
                        <v-icon class="status < 1 ? pending : ">mdi-thumbs-up-down</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-action>
                        <v-icon class="status < 2 ? pending : ">mdi-checkbox-marked-circle</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-action>
                        <v-icon class="status < 3 ? pending : ">mdi-ray-end</v-icon>
                    </v-list-tile-action>

                </v-list-tile>
            </v-list>
        </v-card-text>
        <v-card-actions>
            <v-btn color="primary" flat @click.stop="showDialog=false">Close</v-btn>
        </v-card-actions>
    </v-card>
</v-dialog>
</template>

<script>
    export default {
        data: function () {
            return {
            }
        },
        computed: {
            showDialog: {
                get() {
                    return this.$store.state.voterDialog;
                },
                set(value) {
                    this.$store.commit('voterDialog', value);
                }
            },
        },
        methods:{
            selectVoter: function(id){
                this.$store.commit('changeSelectedVoter', id);
                this.$store.commit('voterDialog', false);
            }
        },
        created() {
        }
    };
</script>