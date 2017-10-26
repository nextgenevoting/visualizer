<template>
    <v-card class="infoCard">

        <span v-if="data.showConfidentiality" tabindex="0" class="ml-0 chip chip--label chip--small lighten-4" v-bind:class="confidentiality == 'private' ? 'red' : 'green'">{{confidentiality}}</span>

        <v-card-title primary-title class="primaryContent">
            <div><span class="label grey--text">{{title}}
              <v-tooltip top>
                <v-icon color="grey lighten-1" slot="activator">info</v-icon><span>Programmatic tooltip</span>
             </v-tooltip></span>
                <div class="value">
                    <slot></slot>
                </div>
            </div>
        </v-card-title>
        <v-card-actions style="height:33px; padding: 0px" v-show="expandable">

            <v-spacer></v-spacer>
            <v-btn icon @click.native="showExpander = !showExpander">
                <v-icon>{{ !showExpander ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
            </v-btn>
        </v-card-actions>
        <v-slide-y-transition v-show="expandable">
            <v-card-text v-show="showExpander">
                <slot name="expandContent">
                </slot>
            </v-card-text>
        </v-slide-y-transition>
    </v-card>
</template>

<script>
    export default {
        data: function () {
            return {
                showExpander: false
            }
        },
        computed: {
            data() {
                return{
                    showConfidentiality: this.$store.state.showConfidentiality
                }
            }
        },
        props: {
            title: {
                type: String,
                required: true,
                default: "Title"
            },
            expandable: {
                type: Boolean,
                required: true,
                default: false
            },
            confidentiality: {
                type: String,
                required: true,
                default: 'public'
            }
        },

        mounted() {
        },
    };
</script>

<style>
    p {
        display: inline;
    }

    .infoCard .primaryContent{
        padding-top: 14px;
    }

    .infoCard .chip {
        position: absolute;
        top: 7px;
        right: 7px;
    }
</style>