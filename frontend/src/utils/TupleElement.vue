<template>
    <div>
   <template  v-for="(element, index) in tupleElement">
     <p v-if="element instanceof Array">{{index+1}} : <TupleElement :tupleElement="element"></TupleElement></p>
     <p v-else><span v-if="tupleElement.length > 1">{{index+1}}:</span>{{element}}</p>
   </template>
    </div>
</template>

<script>
    export default {
      props: {
        tupleElement: {
          type: Array,
          required: true
        }
      }
    }
</script>

<style>

</style>