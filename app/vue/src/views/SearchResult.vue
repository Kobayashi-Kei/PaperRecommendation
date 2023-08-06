<script setup lang="ts">
import { onMounted, ref, watch, watchEffect} from "vue";
import axios from 'axios';
import Header from "@/components/Header.vue";
import SearchForm from "@/components/SearchForm.vue";
import BackToTop from "@/components/BackToTop.vue";
import { useRouter } from "vue-router";
import { useRoute } from 'vue-router'
import type {abstLabelPair, labelScoreOfSimilarity} from '@/type'

const router = useRouter();
const route = useRoute()

// 検索フォームに入力された文字列を取得する
const inputText = ref(route.query.queryText as string);

/**
 * @description 論文のデータ構造
 */
interface Paper {
    title: string;
    abst: string;
    abstSsc: abstLabelPair[];
    author: string;
    publisher: string;
    year: string;
    listShowAbst: string;
    isShowFullAbst: boolean;
    scoreOfSimilarity: number|null;
    labelScoreOfSimilarity: labelScoreOfSimilarity|null;
}

const paperListInit: Paper[] = [] 
const paperList = ref(paperListInit);
const isLoading = ref(true);
const isHighlightLabel = ref(true);

getPaperList();

watch(route, () => {
    inputText.value = route.query.queryText as string;
    getPaperList();
})

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
            if (paperList.value[i].abst.length >= 200) {
                paperList.value[i].listShowAbst = paperList.value[i].abst.substr(0, 200) + " ..."
                paperList.value[i].isShowFullAbst = false
            } else {
                paperList.value[i].listShowAbst = paperList.value[i].abst;
                paperList.value[i].isShowFullAbst = true
            }
        }
        // なんか計算してる風に1.5秒遅延させる
        // await new Promise(resolve => setTimeout(resolve, 1500))
        isLoading.value = false;

        for (let i = 0; i < paperList.value.length; ++i) {
            console.log(paperList.value[i]);
        }

    } catch (error) {
        console.log(error);
        console.log(path)
    }
}
// console.log(`asyncの外: ${paperList.value.length}`)

// const linkClick = ():void => {
//     router.push('/paperDetail');   
// };

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

/**
 * @description 検索結果をJSON形式でダウンロードする
 */
const downloadJSON = () => {
    const blob = new Blob([JSON.stringify(paperList.value, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'paper_list.json';
    a.click();
    a.remove();
};

</script>


<template>
    <Header />
    <SearchForm v-bind:inputText="inputText"/>
    <div class="mt-3 mb-3">
        <p>各論文の <span class="text-blue-500">Read more</span> をクリックすると，全文と観点別の下線を表示します．&nbsp;
                <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="isHighlightLabel" class="sr-only peer">
                    <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                    <span class="ml-3 text-sm font-medium text-gray-900 dark:text-gray-300">下線を表示</span>
                </label>
        </p>
        <p>
            アブストラクトの下線の色は，次のように観点に対応しています．
        </p>
        <span class="label bg">Background</span>, 
        <span class="label obj">Objective</span>,
        <span class="label method">Method</span>,
        <span class="label res">Result</span>,
        <span class="label other">Other</span>
    </div>

    <div class="mt-2 mb-2">
        <button class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center" v-on:click="downloadJSON">
        <svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M13 8V2H7v6H2l8 8 8-8h-5zM0 18h20v2H0v-2z"/></svg>
        <span>検索結果の出力</span>
        </button>
    </div>

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
                    <div>
                        <template v-if="!isHighlightLabel">
                            <p class="mt-2 text-gray-600">{{ paper.abst }}</p>
                        </template>
                        <template v-else v-for="abstLabel in paper.abstSsc" :key="abstLabel[0]">
                            <span v-bind:class="abstLabel[1]" class="label">{{ abstLabel[0] }}</span>&nbsp;
                        </template>
                    </div>
                    <p class="mt-3 text-gray-600">Author: {{ paper.author }}</p>
                    <a @click.prevent.stop="clickFold(index)" class="text-blue-500 hover:underline" href="#">fold</a>
                </template>
            </div>
            <div class="flex justify-between items-center mt-4">
                <div>
                    <div class="items-center text-gray-700">
                        <div v-if="paper.scoreOfSimilarity !== null">Similarity: {{ paper.scoreOfSimilarity }}</div>
                        <div v-if="paper.labelScoreOfSimilarity !== null">
                            <template v-for="(score, label) in paper.labelScoreOfSimilarity" :key="label" >
                                <span class="label" v-bind:class="label">{{ label }}: {{ score }}</span> &nbsp; 
                            </template>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <BackToTop />
</template>

<style scoped>
.label {
    text-decoration:underline;
}
.bg {
    text-decoration-color: blue;
}
.obj {
    text-decoration-color: magenta;
}
.method {
    text-decoration-color: green;
    }
.res {
    text-decoration-color: orange;
}
.other {
     text-decoration-color: darkgrey;
}
</style>