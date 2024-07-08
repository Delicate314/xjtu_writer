import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';
import SearchView from './views/SearchView.vue';
import WriteView from './views/WriteView.vue';
import LoginView from './views/LoginView.vue';
import RegisterView from './views/RegisterView.vue';
import RankView from './views/RankView.vue'
import NovelDetail from './views/NovelDetail.vue'
Vue.use(Router);

export default new Router({
  routes: [
    { path: '/', component: LoginView },
    { path: '/search', component: SearchView },
    { path: '/write', component: WriteView },
    { path: '/login', component: LoginView },
    { path: '/register', component: RegisterView },
    { path: '/Home', component: Home },
    { path: '/Rank', component: RankView },
    { path: '/Novel', component: NovelDetail },
  ],
});
