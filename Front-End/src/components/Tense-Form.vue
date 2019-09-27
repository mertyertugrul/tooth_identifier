<template>
  <b-container class="tense-form">
    <b-row>
      <b-col class="tex-input" md="8">
        <b-form-input v-model="sentence" placeholder="Write a sentence"></b-form-input>
        <hr>
      </b-col>
      <b-col class="button" md="4">
        <b-button variant="outline-primary" v-on:click="tenseIdentifier">Check The Tense</b-button>
      </b-col>
    </b-row>
    <b-row>
      <span class="text-dark">{{ sentence }}</span>
    </b-row>
    <b-row>
      <span class="text-dark">{{add_text}} &nbsp;</span>
      <span class="text-success font-weight-bold">{{tense}}</span>
    </b-row>
  </b-container>
</template>

<script>
import Axios from 'axios';

export default {
  name: 'Tense-Form',
  data() {
    return {
      sentence: '',
      response_json: '',
      tense: '',
      add_text: '',
    };
  },
  methods: {
    tenseIdentifier() {
      Axios.post('http://127.0.0.1:5000/', this.sentence).then((response) => {
        console.log('-----SUCCESS-----');
        console.log(response.data)
        console.log(response.data.Tense);
        this.tense = response.data.Tense;
        this.add_text = 'The tense is: ';
      });
    },
  },
};
</script>

<style scoped>

</style>
