import Vue from 'vue'
import Router from 'vue-router'
import Categories from './components/Categories'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/categories',
            name: 'categories',
            component: Categories
        }
    ]
})