import Vue from 'vue';
import App from './App.vue';
import axios from 'axios'
import router from '@/router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

// 注册全局
// 原型 ---> 原型链 本质是继承
// 显式原型prototype 隐式原型__proto__
// 将axios注册到Vue的原型上，这样在其他组件中就可以通过this.$axios来使用axios
Vue.prototype.$axios = axios
Vue.config.productionTip = false;
Vue.use(ElementUI);

new Vue({
  router:router,
  el: '#app',
  render: h => h(App),
}).$mount('#app');
