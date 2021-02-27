import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export const store = new Vuex.Store({
    state: {
        categoryWeights: []
    },
    mutations: {
        SET_CATEGORY_WEIGHTS (state, categoryWeights) {
            state.categoryWeights = categoryWeights
        }
    },
    actions: {
        loadCategoryWeights ({ commit }) {
            axios
                .get('https://europe-west2-hack-hackasaumon.cloudfunctions.net/api-categories')
                .then(response => {
                    commit('SET_CATEGORY_WEIGHTS', response.data)
                })
        }
    },
    getters: {
        getCategoryWeights: state => {
            console.log(state.categoryWeights)
            return state.categoryWeights
        }
    }
})