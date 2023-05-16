import { createRouter, createWebHistory } from 'vue-router'
import meta from '@/components/meta.vue'
import index_my from '@/components/index_my.vue'
import sign from '@/components/sign.vue'
import gan from '@/components/gan.vue'
import test from '@/components/test.vue'
// import index_my from '@/components/index_my.vue'
const routes = [
    {
        path: "/sign",
        name: "sign",
        component: sign,
    }
    ,{
        path:"/home",
        name:"home",
        component:index_my,
    },
    ,{
        path:"/meta",
        name:"meta",
        component:meta,
    },{
        path:"/gan",
        name:"gan",
        component:gan,
    },{
        path: "/test",
        name: "test",
        component: test,
    },
]
const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router