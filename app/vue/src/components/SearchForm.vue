<script setup lang="ts">
/**
 * 検索フォームの Component
 * 
 * Props: inputText - 検索フォームに表示する文字列
 *
 * Emits: None
 */
import { ref } from "vue";
import { useRouter } from "vue-router";
import { defineProps } from "vue";

const router = useRouter();

interface Props {
    inputText: string;
}
const props = defineProps<Props>();

const query = ref(props.inputText);
const clickSearchBottun = (): void =>{
    console.log("clicked search");
    router.push({path: '/searchResult', query:{queryText:query.value}});     
};

const placeholder = "ex. The aim of this research is to build a model for recommending papers that can explain the reasons for the recommendation. We propose a method based on Abstract Classification and the Paper Embedding Transfomer model."; 
</script>

<template>
    <form class="w-full md:max-w-2xl flex gap-2 pb-3">
        <textarea 
            rows="6"
            class="w-full flex-1 bg-gray-50 text-gray-800 placeholder-gray-500 border focus:ring ring-indigo-300 rounded outline-none transition duration-100 px-3 py-2"
            v-bind:placeholder="placeholder"
            v-model="query"
        ></textarea>
    </form>
    <button 
        class="inline-block bg-indigo-500 hover:bg-indigo-600 active:bg-indigo-700 focus-visible:ring ring-indigo-300 text-white text-sm md:text-base font-semibold text-center rounded outline-none transition duration-100 px-8 py-2 pt"
        v-on:click="clickSearchBottun"
    >
    Search
    </button>
</template>

<style scoped>
</style>