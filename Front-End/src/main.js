import Vue from 'vue';
// eslint-disable-next-line import/extensions,import/no-unresolved
import BootstrapVue from 'bootstrap-vue';
// eslint-disable-next-line import/no-unresolved
import 'bootstrap/dist/css/bootstrap.css';
// eslint-disable-next-line import/no-unresolved
import 'bootstrap-vue/dist/bootstrap-vue.css';
// eslint-disable-next-line import/order,no-unused-vars
import { library } from '@fortawesome/fontawesome-svg-core';
// eslint-disable-next-line no-unused-vars
import { faUserSecret } from '@fortawesome/free-solid-svg-icons';
// eslint-disable-next-line no-unused-vars
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import router from './router';
import App from './App.vue';


library.add(faUserSecret);

Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.use(BootstrapVue);

Vue.config.productionTip = false;


new Vue({
  router,
  render: h => h(App),
  // el: '#app',
  // components: { App },
  // template: '<App/>',
}).$mount('#app');
