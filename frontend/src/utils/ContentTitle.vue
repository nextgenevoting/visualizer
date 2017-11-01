<template>
    <div class="layout row wrap">
        <div class="contentHeader">
            <v-icon>{{ icon }}</v-icon>
        </div>
        <h3 class="my-3">{{ title}}</h3>
    </div>
</template>
<script>
    export default {
        props: {
            title: {
                type: String,
                required: true,
                default: "NoTitle"
            },
            icon: {
                type: String,
                required: true,
                default: ""
            },
        },
        mounted() {
        },
    };
</script>

<style>
    .contentHeader{
        float: left;font-size: 38px; color: #505050; width:60px
    }

    .contentHeader .icon{
        font-size: 36px;
        color: #505050 !important;
        margin-top: 18px;
    }

    .my-3{
        color: #505050;  font-size: 32px;
    }
</style>