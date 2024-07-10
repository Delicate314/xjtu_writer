import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/views/Home.vue';
import SearchView from '@/views/SearchView.vue';
import WriteView from '@/views/WriteView.vue';
import LoginView from '@/views/LoginView.vue';
import RegisterView from '@/views/RegisterView.vue';
import RankView from '@/views/RankView.vue'
import NovelDetail from '@/views/NovelDetail.vue'
Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/Home',
            component: Home,
            meta: {
                name: '首页',
                isShow: true
            },
        },
        {
            path: '/',
            component: LoginView,
            meta: {
                name: '登录',
                isShow: false
            },
        },
        {
            path: '/search',
            component: SearchView,
            meta: {
                name: '搜索',
                isShow: true
            },
        },
        {
            path: '/write',
            component: WriteView,
            meta: {
                name: '写小说',
                isShow: true
            },
        },
        {
            path: '/register',
            component: RegisterView,
            meta: {
                name: '注册',
                isShow: false
            },
        },
        {
            path: '/Rank',
            component: RankView,
            meta: {
                name: '排行榜',
                isShow: true
            },
        },
        {
            path: '/Novel',
            component: NovelDetail,
            meta: {
                name: '小说详情',
                isShow: false
            },
        },
    ],
});
