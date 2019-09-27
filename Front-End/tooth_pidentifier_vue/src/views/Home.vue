
<template>
  <div class="home">
    <link rel="stylesheet" href="../../node_modules/@fortawesome/fontawesome-free/css/all.css">
    <b-container class="main">
      <b-row class="page-wrapper">
        <SearchForm/>
      </b-row>
    </b-container>
  </div>
</template>

<script>
// @ is an alias to /src


// eslint-disable-next-line import/extensions
import SearchForm from '@/components/Search-Form';

export default {
  name: 'home',
  components: {
    SearchForm,
  },
  data() {
    return {
      title: 'Tooth Identifier',
      developer: 'Mert Y. Ertugrul',
    };
  },
};
</script>

<style scoped>
  @import "../styleSheet.css";
  @import "../../node_modules/@fortawesome/fontawesome-free/css/all.css";
  /*<link rel="stylesheet" href="../../node_modules/@fortawesome/fontawesome-free/css/all.css">*/

</style>
