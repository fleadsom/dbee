import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import router from './router.js'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import VueRouter from 'vue-router'
import axios from 'axios'

window.axios = require('axios')
axios.defaults.baseURL = 'https://europe-west2-hack-hackasaumon.cloudfunctions.net'

Vue.use(VueRouter)

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
