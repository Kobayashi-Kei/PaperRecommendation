<script setup lang="ts">
import { ref } from "vue";
import type { abstLabelPair, labelScoreOfSimilarity } from '@/type'
import axios from 'axios';
import Loading from "@/components/Loading.vue";
import LabeledAbst from "@/components/LabeledAbst.vue";
import ExplainLabel from "@/components/ExplainLabel.vue";
import { settings } from "@/settings";

const inputAbst = ref("");
const labeledAbstInit: abstLabelPair[] = []; 
const labeledAbst = ref(labeledAbstInit);
const isLoading = ref(false);
const placeholder = "Abstract ..."

/**
 * @description アブスト分類を行う
 */
async function getAbstClassification() {
    isLoading.value = true
    console.log(`getAbstClassification(): ${inputAbst.value}`);
    const path = `http://${settings.ip_address}:${settings.port}/classify`;
    
    const params = {
        abst: inputAbst.value
    };
    try {
        const response = await axios.post(path, params);
        labeledAbst.value = response.data;
        isLoading.value = false;
    } catch (error) {
        console.log(error);
        console.log(path)
    }
}

const onClickClassificationButton = (): void => {
    console.log("clicked classify");
    console.log(`inputAbst: ${inputAbst.value}`);
    getAbstClassification();
};

</script>

<template>
<div class="mb-6 flex items-end justify-between gap-4">
        <h2 class="text-2xl font-bold text-gray-800 lg:text-3xl">Abstract Classification</h2>
        <!-- <a href="#" class="inline-block rounded-lg border bg-white px-4 py-2 text-center text-sm font-semibold text-gray-500 outline-none ring-indigo-300 transition duration-100 hover:bg-gray-100 focus-visible:ring active:bg-gray-200 md:px-8 md:py-3 md:text-base">Show more</a> -->
</div>
<div class="mb-3">
    <ExplainLabel />
</div>
<div class="flex gap-4">
    <!-- Input Section -->
    <div class="flex-1 flex flex-col gap-2">
        <form class="w-full flex flex-col gap-2 pb-3">
            <textarea 
                rows="6"
                class="w-full bg-gray-50 text-gray-800 placeholder-gray-500 border focus:ring ring-indigo-300 rounded outline-none transition duration-100 px-3 py-2"
                v-bind:placeholder="placeholder"
                v-model="inputAbst"
            ></textarea>
            <div v-if="isLoading" class="mt-4 flex justify-center">
                <Loading />
            </div>
            <button v-else 
                class="bg-indigo-500 hover:bg-indigo-600 active:bg-indigo-700 focus-visible:ring ring-indigo-300 text-white text-sm md:text-base font-semibold text-center rounded outline-none transition duration-100 px-8 py-2"
                v-on:click.prevent="onClickClassificationButton"
            >
            Classify
            </button>
        </form>
    </div>
    <!-- Output Section -->
    <div class="flex-1 bg-gray-50 border rounded p-3">
        <LabeledAbst v-bind:labeledAbst="labeledAbst"  v-bind:is-limited-length="false"/>
    </div>
</div>

</template>