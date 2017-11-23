<template>
    <span>
   <template  v-for="(element, index) in tupleElement">
     <p v-if="element instanceof Array">
         <TupleElement :tupleElement="element"></TupleElement>
     </p>
     <p v-else>
         {{index+1}}: {{ element }}
     </p>
   </template>
    </span>
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