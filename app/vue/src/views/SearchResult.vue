<script setup lang="ts">
import { onMounted, ref, watch, watchEffect} from "vue";
import axios from 'axios';
import Header from "@/components/Header.vue";
import SearchForm from "@/components/SearchForm.vue";
import BackToTop from "@/components/BackToTop.vue";
import { useRouter } from "vue-router";
import { useRoute } from 'vue-router'

const router = useRouter();
const route = useRoute()

const inputText = ref(route.query.queryText as string);

// console.log(inputText)
interface Paper {
    title: string;
    abst: string;
    author: string;
    publisher: string;
    year: string;
    listShowAbst: string;
    isShowFullAbst: boolean;
}
const paperListInit: Paper[] = [] 
const paperList = ref(paperListInit);
const isLoading = ref(true);
function resolve() {
    console.log("Delayed for 3 second.");
}
/**
 * @description 論文検索結果を取得する
 */
async function getPaperList() {
    isLoading.value = true
    console.log(`getPaperList(): ${inputText.value}`);
    const path = 'http://localhost:5050/search';
    const params = {
        query: inputText.value
    };
    try {
        const res = await axios.post(path, params);
        paperList.value = res.data;
        // TODO: Piniaデータストアに格納

        for (let i = 0; i < paperList.value.length; ++i) {
            // console.log(paperList.value[i].abst)
            if (paperList.value[i].abst.length >= 200){
                paperList.value[i].listShowAbst = paperList.value[i].abst.substr(0,200) + " ..."
                paperList.value[i].isShowFullAbst = false
            } else {
                paperList.value[i].listShowAbst = paperList.value[i].abst;
                paperList.value[i].isShowFullAbst = true
            }
        }    
        // なんか計算してる風に1.5秒遅延させる
        // await new Promise(resolve => setTimeout(resolve, 1500))
        isLoading.value = false;
    } catch (error) {
        console.log(error);
        console.log(path)
    }
}
getPaperList();

watch(route, () => {
    inputText.value = route.query.queryText as string;
    getPaperList();
})

// console.log(`asyncの外: ${paperList.value.length}`)

const linkClick = ():void => {
    router.push('/paperDetail');   
};

/**
 * @description 論文の概要を全文表示する
 * @param index 
 */
const clickReadMore = (index: number):void => {
    paperList.value[index].isShowFullAbst = true
};

/**
 * @description 論文の概要を折りたたむ
 * @param index 
 */
const clickFold = (index: number):void => {
    paperList.value[index].isShowFullAbst = false
};
</script>

<template>
    <Header />
    <SearchForm v-bind:inputText="inputText"/>

    <div v-if="isLoading" class="flex justify-center">
        <div class="animate-ping h-2 w-2 bg-blue-600 rounded-full"></div>
        <div class="animate-ping h-2 w-2 bg-blue-600 rounded-full mx-4"></div>
        <div class="animate-ping h-2 w-2 bg-blue-600 rounded-full"></div>
    </div>
    <div v-else v-for="paper, index in paperList" class="pb-4">
        <div class="max-w-4xl px-10 py-6 bg-white rounded-lg shadow-md">
            <div class="flex justify-between items-center">
                <span class="font-light text-gray-600">{{ paper.year }}</span>
                <p class="px-2 py-1 bg-gray-600 text-gray-100 font-bold rounded hover:bg-gray-500">{{ paper.publisher }}</p>
            </div>
            <div class="mt-2">
                <!-- 論文の詳細表示をする場合はaタグを使う -->
                <!-- <a class="text-2xl text-gray-700 font-bold hover:underline" href="#" @click.prevent.stop="linkClick"
                    >{{ paper.title }}
                </a> -->
                <p class="text-2xl text-gray-700 font-bold" href="#">{{ paper.title }}</p>
                <template v-if="!paper.isShowFullAbst">
                    <p class="mt-2 text-gray-600">{{ paper.listShowAbst }}</p>
                    <a @click.prevent.stop="clickReadMore(index)" class="text-blue-500 hover:underline" href="#">Read more</a>
                </template>
                <template v-else>
                    <p class="mt-2 text-gray-600">{{ paper.abst }}</p>
                    <p class="mt-3 text-gray-600">Author: {{ paper.author }}</p>
                    <a @click.prevent.stop="clickFold(index)" class="text-blue-500 hover:underline" href="#">fold</a>
                </template>
            </div>
            <div class="flex justify-between items-center mt-4">
                <div>
                    <div class="flex items-center" href="#">
                        <!-- <h1 class="text-gray-700 text-2xl">{{ paper.author }}</h1> -->
                    </div>
                </div>
            </div>
        </div>
    </div>
    <BackToTop />
</template>

<style scoped>
</style>