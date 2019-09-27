<template>
  <div class="home">
    <link rel="stylesheet" href="../../node_modules/@fortawesome/fontawesome-free/css/all.css">
    <b-container class="main">
      <b-row class="page-wrapper">
        <TenseForm/>
      </b-row>
    </b-container>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars,import/extensions
import TenseForm from '@/components/Tense-Form';

export default {
  name: 'Tense',
  components: {
      TenseForm,
  },
};
</script>

<style scoped>

</style>
