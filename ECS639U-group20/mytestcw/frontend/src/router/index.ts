import {createRouter, createWebHistory} from 'vue-router'
import Home from '/src/views/Home.vue'
import UserProfile from '/src/views/UserProfile.vue'
import Item from '/src/views/Item.vue'
import Posting from '/src/views/Posting.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/userprofile',
        name: 'Profile',
        component: UserProfile
    },
    {
        path: '/item/:id',
        component: Item,
        name: 'Item',
        props: true
    },
    {
        path: '/post',
        component: Posting,
        name: 'Posting',
        props: true
    },
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URLs),
    routes
})

export default router