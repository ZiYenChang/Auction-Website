<template>
  <Navbar />
  <div id="mainBody">
    <router-view></router-view>
  </div>
  
</template>

<script lang="ts">
import Navbar from './components/Navbar.vue';

export default{
  components:{
    Navbar
  },
}
</script>

<style>
div#app {
    width: 100%;
  vertical-align: baseline;
}

#mainBody{
  width: 80%;
  margin: 0 10%;
}
</style>
