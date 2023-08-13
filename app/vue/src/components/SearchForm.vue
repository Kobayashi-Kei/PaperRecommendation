<script setup lang="ts">
/**
 * 検索フォームの Component
 * 
 * Props: inputText - 検索フォームに表示する文字列
 *
 * Emits: None
 */
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import { defineProps } from "vue";
import type { eventYearList } from "@/type";
import { useFiltersStore } from "@/stores/filters";

const router = useRouter();
const filterStore = useFiltersStore();

interface Props {
    inputText: string;
}
const props = defineProps<Props>();

const query = ref(props.inputText);
const selectedEvent = ref('all');
const selectedYear = ref('all');
const eventYearListInit: eventYearList = {};
const eventYearLists = ref(eventYearListInit);
const yearList = ref([] as string[]);

/**
 * @description 検索の絞り込み条件はイベントと年の2つあり，データセットに依存するため
 *              Store経由でサーバサイドから取得する
 */
const setConditionDropDown = async () => {
    const currentEventYearList = filterStore.getEventYearList;

    // 初期はサーバから絞り込み条件を取得
    if (Object.keys(currentEventYearList).length === 0) {
        await filterStore.getSearchCond();
        eventYearLists.value = filterStore.getEventYearList;
    } else {
        selectedEvent.value = filterStore.currentEventFilter;
        selectedYear.value = filterStore.currentYearFilter;
        eventYearLists.value = filterStore.getEventYearList;
    }
    console.log(selectedEvent.value);
    yearList.value = eventYearLists.value[selectedEvent.value];
    
    // console.log("eventYearLists: " + eventYearLists.value);
    // console.log("yearList: " + yearList.value);
};
setConditionDropDown();


/**
 * @description イベントが選択されたそのイベントの年リストを取得し，セットする
 */
watch(selectedEvent, () => {
    // console.log("selectedEvent: " + selectedEvent.value);
    filterStore.setEventFilter(selectedEvent.value);
    yearList.value = eventYearLists.value[selectedEvent.value]
    // 現在setされている year がそのeventの year リストになければ，allにする
    if (!yearList.value.includes(filterStore.currentYearFilter)) {
        selectedYear.value = 'all';
    }
    console.log("set event: " + filterStore.currentEventFilter);
});

/**
 * @description 年が選択されたら，その年をセットする
 */
watch(selectedYear, () => {
    filterStore.setYearFilter(selectedYear.value);
    console.log("set year: " + filterStore.currentYearFilter);
});

const clickSearchBottun = (): void =>{
    console.log("clicked search");
    router.push({path: '/searchResult', query:{queryText:query.value}});     
};

const placeholder = "ex. The aim of this research is to build a model for recommending papers that can explain the reasons for the recommendation. We propose a method based on Abstract Classification and the Paper Embedding Transfomer model."; 
</script>

<template>
    <!-- Textarea -->
    <form class="">
        <textarea 
            rows="6"
            class="w-full bg-gray-50 text-gray-800 placeholder-gray-500 border focus:ring ring-indigo-300 rounded outline-none transition duration-100 px-0 py-2"
            v-bind:placeholder="placeholder"
            v-model="query"
        ></textarea>
    </form>

    <!-- Search Button -->
    <div class="flex">
        <div class="px-2 flex flex-row-reverse">
            <div class="mb-1 px-2">
                <label for="yearFilter" class="block text-gray-700">Year:</label>
                <select v-model="selectedYear" id="yearFilter" class="mt-1 rounded-md border-gray-300">
                    <option v-for="year in yearList" :key="year" :value="year">{{ year }}</option>
                </select>
            </div>

            <div class="mb-1 px-2">
                <label for="eventFilter" class="block text-gray-700">Event:</label>
                <select v-model="selectedEvent" class="mt-1 rounded-md border-gray-300">
                    <option v-for="(years, event) in eventYearLists" :key="event" :value="event">{{ event }}</option>
                </select>
            </div>
            
            <span><img src="@/assets/511_s_f.png" alt="絞り込みアイコン" width="40"></span>
        </div>
        <button 
        class="bg-indigo-500 hover:bg-indigo-600 active:bg-indigo-700 focus-visible:ring ring-indigo-300 text-white text-sm md:text-base font-semibold text-center rounded outline-none transition duration-100 px-8 py-2"
        v-on:click="clickSearchBottun"
        >
        Search
        </button>
    </div>
</template>

<style scoped>
</style>