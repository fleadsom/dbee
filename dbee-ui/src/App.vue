<template>
  <div id="app">
    <navigation/>
    <router-view/>
  </div>
</template>

<script>
import Navigation from './components/Navigation.vue'
export default {
  name: 'App',
  components: {
    Navigation
  }
}
</script>
