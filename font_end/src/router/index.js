import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/views/Home.vue';
import SearchView from '@/views/SearchView.vue';
import WriteView from '@/views/WriteView.vue';
import LoginView from '@/views/LoginView.vue';
import RegisterView from '@/views/RegisterView.vue';
import RankView from '@/views/RankView.vue';
import NovelDetail from '@/views/NovelDetail.vue';
import Admin from '@/views/backend_views/admin_home.vue';

Vue.use(Router);

const router = new Router({
    routes: [
        {
            path: '/Home',
            component: Home,
            meta: {
                name: '首页',
                isShow: true,
                requiresAuth: true, // 添加需要认证的标记
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
                isShow: true,
                background: 'writing-background.jpg',
                requiresAuth: true, // 添加需要认证的标记
            },
        },
        {
            path: '/write',
            component: WriteView,
            meta: {
                name: '写小说',
                isShow: true,
                background: 'writing-background.jpg',
                requiresAuth: true, // 添加需要认证的标记
            },
        },
        {
            path: '/login',
            component: LoginView,
            meta: {
                name: '登录',
                isShow: false,
                background: 'login-background.png',
                requiresAuth: false, // 添加需要认证的标记
            },
        },
        {
            path: '/register',
            component: RegisterView,
            meta: {
                name: '注册',
                isShow: false,
                background: 'register-background.png',
                requiresAuth: false, // 添加需要认证的标记
            },
        },
        {
            path: '/rank',
            component: RankView,
            meta: {
                name: '排行榜',
                isShow: true,
                background: 'writing-background.jpg',
                requiresAuth: true, // 添加需要认证的标记
            },
        },
        {
            path: '/Novel',
            component: NovelDetail,
            meta: {
                name: '小说详情',
                isShow: false,
                background: 'writing-background.jpg',
                requiresAuth: true, // 添加需要认证的标记
            },
        },
        {
            path: '/Admin',
            component: Admin,
            meta: {
                name: '用户管理页面',
                isShow: false,
                requiresAuth: true, // 添加需要认证的标记
            },
        }
    ],
});

router.beforeEach((to, from, next) => {
    
    const isAuthenticated = window.sessionStorage.getItem('passport'); // 检查用户是否已登录
    
    if (to.matched.some(record => record.meta.requiresAuth)) {
        // 如果目标路由需要认证并且用户没有登录
        if (!isAuthenticated) {
            next({
                path: '/',  replace: true ,
                 
            });
        } else {
            next(); 
        }
    } else {
        next(); 
    }
});

export default router;