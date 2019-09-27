<template>
  <b-container class="search-form">
    <b-row>
      <b-col class="text-input" md="8">
        <b-form-textarea rows="25" v-model="text" placeholder="Give me the book..."
        ></b-form-textarea>
      </b-col>
      <b-col class="search-button" md="4">
        <b-button variant="outline-primary" v-on:click="getText" class="btn-block">Analyze
          The Book</b-button>
        <hr>
        <div>
          <b-form-group
            label="Filter"
            label-cols-sm="2"
            label-align-sm="right"
            label-size="sm"
            label-for="filterInput"
            class="mb-0"
          >
            <b-input-group size="sm">
              <b-form-input
                v-model="filter"
                type="search"
                id="filterInput"
                placeholder="Type to Search"
                class="mb-2 mr-sm-2 mb-sm-0"
              ></b-form-input>
              <b-input-group-append>
                <b-button :disabled="!filter" @click="filter = ''" class="btn-sm">Clear</b-button>
              </b-input-group-append>
            </b-input-group>
          </b-form-group>

          <b-table striped hover sticky-header="495px" :items="items" :fields="fields"
                   :busy="isBusy"
                   :tbody-tr-class="rowClass" class="mt-3" :filter="filter"
                   @filtered="onFiltered" outlined>
            <template v-slot:table-busy>
              <div class="text-center text-danger my-2">
                <b-spinner class="align-middle"></b-spinner>
                <strong>Loading...</strong>
              </div>
              <span>Depending the size of the text this might take couple of minutes</span>
            </template>
          </b-table>
        </div>
      </b-col>
    </b-row>
    <!--    <b-row>
          <div class="mt-2">Word: {{ text }}</div>
        </b-row>-->
    <hr>
  </b-container>
</template>

<script>
import Axios from 'axios';

export default {
  name: 'Search-form',
  data() {
    return {
      filter: null,
      filterOn: [],
      isBusy: false,
      text: '',
      value: '',
      posts: [],
      lorem: [],
      results: [],
      definations: [],
      meanings: [],
      gotError: false,
      error: '',
      number_of_sentence: '',
      number_of_words: '',
      number_of_characters: '',
      words_per_sentence: '',
      characters_per_words: '',
      sentence_per_paragraph: '',
      number_of_sylables: '',
      syllables_per_word: '',
      number_of_monosyllable: '',
      monosyllable_per_word: '',
      number_of_complex_words: '',
      complex_words_per_word: '',
      advance_words_per_words: '',
      number_of_advance_words: '',
      number_of_common_words: '',
      common_words_per_words: '',
      number_of_unknown_words: '',
      verbs_per_word: '',
      dale_chall_score: '',
      flesch_reading_ease_score: '',
      new_flesch_reading_ease_score: '',
      gunning_fog_score: '',
      smog_score: '',
      forcast_score: '',
      ari_score: '',
      coleman_liau_score: '',
      lix_score: '',
      rix_score: '',
      power_summer_kearl: '',
      spache_score: '',
      linsear_write: '',
      response_json: {},
      prediction_json: {},
      fields: [
        {
          key: 'field',
          sortable: true,
        },
        {
          key: 'parameter',
          sortable: true,
        },
      ],
      items: [
        {
          field: 'Level of the Book',
          parameter: this.prediction_json,
          status: 'awesome',
          rowClass: 'font-weight-bold',
        },
        {
          field: 'Number of Sentence',
          parameter: this.number_of_sentence,
        },
        {
          field: 'Number of Word',
          parameter: this.number_of_words,
        },
        {
          field: 'Number of Characters',
          parameter: this.number_of_characters,
        },
        {
          field: 'Words per 100 Sentences',
          parameter: this.words_per_sentence,
        },
        {
          field: 'Characters per 100 Words',
          parameter: this.characters_per_words,
        },
        {
          field: 'Sentence per 100 Paragraphs',
          parameter: this.sentence_per_paragraph,
        },
        {
          field: 'Number of Syllables',
          parameter: this.number_of_sylables,
        },
        {
          field: 'Syllables per 100 Words',
          parameter: this.syllables_per_word,
        },
        {
          field: 'Number of Monosyllables',
          parameter: this.number_of_monosyllable,
        },
        {
          field: 'Monosyllable per Word',
          parameter: this.monosyllable_per_word,
        },
        {
          field: 'Number of Complex Words',
          parameter: this.number_of_complex_words,
        },
        {
          field: 'Complex Words per 100 Words',
          parameter: this.complex_words_per_word,
        },
        {
          field: 'Number of Advance Words',
          parameter: this.number_of_advance_words,
        },
        {
          field: 'Advance Words per 100 Words',
          parameter: this.advance_words_per_words,
        },
        {
          field: 'Number of Common Words',
          parameter: this.number_of_common_words,
        },
        {
          field: 'Common Words per 100 Words',
          parameter: this.common_words_per_words,
        },
        {
          field: 'Verbs per 100 Words',
          parameter: this.verbs_per_word,
        },
        {
          field: 'Number of Unknown verbs',
          parameter: this.number_of_unknown_words,
        },
        {
          field: 'Dale Chall Score',
          parameter: this.dale_chall_score,
        },
        {
          field: 'Flesch Reading Ease Score',
          parameter: this.flesch_reading_ease_score,
        },
        {
          field: 'New Flesch Reading Ease Score',
          parameter: this.new_flesch_reading_ease_score,
        },
        {
          field: 'Gunning Fog Score',
          parameter: this.gunning_fog_score,
        },
        {
          field: 'SMOG Score',
          parameter: this.smog_score,
        },
        {
          field: 'FORCAST Score',
          parameter: this.forcast_score,
        },
        {
          field: 'ARI Score',
          parameter: this.ari_score,
        },
        {
          field: 'Coleman Liau Score',
          parameter: this.coleman_liau_score,
        },
        {
          field: 'LIX Score',
          parameter: this.lix_score,
        },
        {
          field: 'RIX Score',
          parameter: this.rix_score,
        },
        {
          field: 'Powers Sumner Kearl',
          parameter: this.power_summer_kearl,
        },
        {
          field: 'Spache Score',
          parameter: this.spache_score,
        },
        {
          field: 'Linsear Write',
          parameter: this.linsear_write,
        },
        {
          key: 'isActive',
          label: 'is Active',
          formatter: (value, key, item) => (value ? 'Yes' : 'No'),
          sortable: true,
          sortByFormatted: true,
          filterByFormatted: true,
        },
      ],
    };
  },
  watch: {
    prediction_json() {
      this.items[0].parameter = this.prediction_json;
      this.$set(this.items, 0, this.items[0]);
    },
    number_of_sentence() {
      this.items[1].parameter = this.number_of_sentence;
      this.$set(this.items, 1, this.items[1]);
    },
    number_of_words() {
      this.items[2].parameter = this.number_of_words;
      this.$set(this.items, 2, this.items[2]);
    },
    number_of_characters() {
      this.items[3].parameter = this.number_of_characters;
      this.$set(this.items, 3, this.items[3]);
    },
    words_per_sentence() {
      this.items[4].parameter = this.words_per_sentence;
      this.$set(this.items, 4, this.items[4]);
    },
    characters_per_words() {
      this.items[5].parameter = this.characters_per_words;
      this.$set(this.items, 5, this.items[5]);
    },
    sentence_per_paragraph() {
      this.items[6].parameter = this.sentence_per_paragraph;
      this.$set(this.items, 6, this.items[6]);
    },
    number_of_sylables() {
      this.items[7].parameter = this.number_of_sylables;
      this.$set(this.items, 7, this.items[7]);
    },
    syllables_per_word() {
      this.items[8].parameter = this.syllables_per_word;
      this.$set(this.items, 8, this.items[8]);
    },
    number_of_monosyllable() {
      this.items[9].parameter = this.number_of_monosyllable;
      this.$set(this.items, 9, this.items[9]);
    },
    monosyllable_per_word() {
      this.items[10].parameter = this.monosyllable_per_word;
      this.$set(this.items, 10, this.items[10]);
    },
    number_of_complex_words() {
      this.items[11].parameter = this.number_of_complex_words;
      this.$set(this.items, 11, this.items[11]);
    },
    complex_words_per_word() {
      this.items[12].parameter = this.complex_words_per_word;
      this.$set(this.items, 12, this.items[12]);
    },
    advance_words_per_words() {
      this.items[14].parameter = this.advance_words_per_words;
      this.$set(this.items, 14, this.items[14]);
    },
    number_of_advance_words() {
      this.items[13].parameter = this.number_of_advance_words;
      this.$set(this.items, 13, this.items[13]);
    },
    number_of_common_words() {
      this.items[15].parameter = this.number_of_common_words;
      this.$set(this.items, 15, this.items[15]);
    },
    common_words_per_words() {
      this.items[16].parameter = this.common_words_per_words;
      this.$set(this.items, 16, this.items[16]);
    },
    verbs_per_word() {
      this.items[17].parameter = this.verbs_per_word;
      this.$set(this.items, 17, this.items[17]);
    },
    number_of_unknown_words() {
      this.items[18].parameter = this.number_of_unknown_words;
      this.$set(this.items, 18, this.items[18]);
    },
    dale_chall_score() {
      this.items[19].parameter = this.dale_chall_score;
      this.$set(this.items, 19, this.items[19]);
    },
    flesch_reading_ease_score() {
      this.items[20].parameter = this.flesch_reading_ease_score;
      this.$set(this.items, 20, this.items[20]);
    },
    new_flesch_reading_ease_score() {
      this.items[21].parameter = this.new_flesch_reading_ease_score;
      this.$set(this.items, 21, this.items[21]);
    },
    gunning_fog_score() {
      this.items[22].parameter = this.gunning_fog_score;
      this.$set(this.items, 22, this.items[22]);
    },
    smog_score() {
      this.items[23].parameter = this.smog_score;
      this.$set(this.items, 23, this.items[23]);
    },
    forcast_score() {
      this.items[24].parameter = this.forcast_score;
      this.$set(this.items, 24, this.items[24]);
    },
    ari_score() {
      this.items[25].parameter = this.ari_score;
      this.$set(this.items, 25, this.items[25]);
    },
    coleman_liau_score() {
      this.items[26].parameter = this.coleman_liau_score;
      this.$set(this.items, 26, this.items[26]);
    },
    lix_score() {
      this.items[27].parameter = this.lix_score;
      this.$set(this.items, 27, this.items[27]);
    },
    rix_score() {
      this.items[28].parameter = this.rix_score;
      this.$set(this.items, 28, this.items[28]);
    },
    power_summer_kearl() {
      this.items[29].parameter = this.power_summer_kearl;
      this.$set(this.items, 29, this.items[29]);
    },
    spache_score() {
      this.items[30].parameter = this.spache_score;
      this.$set(this.items, 30, this.items[30]);
    },
    linsear_write() {
      this.items[31].parameter = this.linsear_write;
      this.$set(this.items, 31, this.items[31]);
    },
  },
  computed: {
    sortOptions() {
      // Create an options list from our fields
      return this.fields
        .filter(f => f.sortable)
        .map(f => ({ text: f.label, value: f.key }));
    },
  },
  methods: {
    getText() {
      this.isBusy = true;
      Axios.post('http://127.0.0.1:5000/', this.text).then((response) => {
        console.log('-----SUCCESS-----');
        this.response_json = JSON.parse(response.data);
        this.prediction_json = this.response_json.Prediction;
        this.prediction_json = this.predictionTranslator(this.prediction_json);
        console.log(this.prediction_json);
        console.log(this.response_json['0']);
        this.response_json = this.response_json['0'];
        this.number_of_sentence = this.response_json['Number of Sentence'];
        this.number_of_words = this.response_json['Number of Words'];
        this.number_of_characters = this.response_json['Number of Characters'];
        this.words_per_sentence = this.response_json['Words per Sentence (%)'];
        this.characters_per_words = this.response_json['Character per Words (%)'];
        this.sentence_per_paragraph = this.response_json['Sentence per Paragraph (%)'];
        this.number_of_sylables = this.response_json['Number of Sylables'];
        this.syllables_per_word = this.response_json['Syllables per Word (%)'];
        this.number_of_monosyllable = this.response_json['Number of Monosyllable'];
        this.monosyllable_per_word = this.response_json['Monosyllable per Word (%)'];
        this.number_of_complex_words = this.response_json['Number of Complex Words'];
        this.complex_words_per_word = this.response_json['Complex Words per Word (%)'];
        this.number_of_advance_words = this.response_json['Number of Advance Words'];
        this.advance_words_per_words = this.response_json['Advance Words per Words (%)'];
        this.number_of_common_words = this.response_json['Number of Common Words'];
        this.common_words_per_words = this.response_json['Common Words per Words (%)'];
        this.verbs_per_word = this.response_json['Verbs per Words (%)'];
        this.number_of_unknown_words = this.response_json['Number of Unknown Words'];
        this.dale_chall_score = this.response_json['Dale Chall Score'];
        this.flesch_reading_ease_score = this.response_json['Flesch Reading Ease Score'];
        this.new_flesch_reading_ease_score = this.response_json['New Flesch Reading Ease Score'];
        this.gunning_fog_score = this.response_json['Gunning Fog Score'];
        this.smog_score = this.response_json['SMOG Score'];
        this.forcast_score = this.response_json['FORCAST Score'];
        this.ari_score = this.response_json['ARI Score'];
        this.coleman_liau_score = this.response_json['Coleman Liau Score'];
        this.lix_score = this.response_json['LIX Score'];
        this.rix_score = this.response_json['RIX Score'];
        this.power_summer_kearl = this.response_json['Powers Sumner Kearl'];
        this.spache_score = this.response_json['Spache Score'];
        this.linsear_write = this.response_json['Linsear Write'];
        this.isBusy = false;
      });
    },
    rowClass(item, type) {
      if (!item) return;
      if (item.status === 'awesome') return 'table-success font-weight-bold';
    },
    predictionTranslator(pre) {
      if (pre == '[0]') {
        return 'Beginner';
      }
      if (pre == '[1]') {
        return 'Elementary';
      }
      if (pre == '[2]') {
        return 'Intermediate';
      }
      if (pre == '[3]') {
        return 'Upper-Intermediate';
      }
      if (pre == '[4]') {
        return 'Advance';
      }
    },
  },

};
</script>

<style scoped>
  @import "../styleSheet.css";
</style>
