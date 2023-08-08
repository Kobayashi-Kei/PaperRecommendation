<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const activeLink = ref("Home");
const isOpenedMenu = ref(false);

const onClickLink = (name: string): void => {
  activeLink.value = name;
  router.push({name: name})
  isOpenedMenu.value = false;
};

const onClickMenu = (): void => {
  isOpenedMenu.value = !isOpenedMenu.value;
};

const url_name = location.href.split("/").pop();
// console.log(url_name);
if (url_name == "abstClassification") {
  activeLink.value = "AbstClassification";
} else {
  activeLink.value = "Home";
}

</script>

<template>
<!-- <header class="flex justify-between items-center py-4 md:py-8 mb-8 md:mb-12 xl:mb-16"> -->
<header class="flex justify-between items-center py-4 md:py-8 ">
      <!-- logo - start -->
      <a href="/" class="inline-flex items-center text-black-800 text-2xl md:text-3xl font-bold gap-2.5" aria-label="logo">
        <img width="95" height="94" viewBox="0 0 95 94" class="w-6 h-auto text-indigo-500" fill="currentColor" src="../assets/document.svg">
        Paper Recommendation
      </a>
      <!-- logo - end -->

      <!-- nav - start -->
      <nav class="hidden gap-12 lg:flex">
          <a href="#" v-on:click.prevent.stop="onClickLink('Home')" v-bind:class="[activeLink == 'Home' ? 'text-indigo-500' : 'text-gray-600']" class="link">Paper Recommendation</a>
          <a href="#" v-on:click.prevent.stop="onClickLink('AbstClassification')" v-bind:class="[activeLink == 'AbstClassification' ? 'text-indigo-500' : 'text-gray-600']" class="link">Abstract Classification</a>
      </nav>
      <!-- nav - end -->

      <!-- buttons - start -->
      <button type="button" v-on:click="onClickMenu()" class="inline-flex items-center lg:hidden bg-gray-200 hover:bg-gray-300 focus-visible:ring ring-indigo-300 text-gray-500 active:text-gray-700 text-sm md:text-base font-semibold rounded-lg gap-2 px-2.5 py-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd" />
        </svg>
        Menu
      </button>
      <!-- buttons - end -->

      <!-- menu for smartphone - start -->
        <div v-if="isOpenedMenu" class="absolute top-0 left-0 w-full h-full bg-white z-10">        
          <button type="button" v-on:click="onClickMenu()" class="absolute top-4 right-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
          <div class="flex flex-col items-center justify-center h-full gap-8">
            <a href="#" v-on:click.prevent.stop="onClickLink('Home')" class="text-2xl font-bold text-gray-800">Home</a>
            <a href="#" v-on:click.prevent.stop="onClickLink('AbstClassification')" class="text-2xl font-bold text-gray-800">Abstract Classification</a>
          </div>
        </div>
        <!-- menu for smartphone - end -->
    </header>

</template>

<style scoped>
.link {
  @apply text-lg font-semibold transition duration-100 hover:text-indigo-500 active:text-indigo-700;
}
</style>


