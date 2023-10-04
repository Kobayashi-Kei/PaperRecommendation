<script setup lang="ts">
import { ref, defineProps, watch } from "vue";
import type { abstLabelPair } from '@/type'

interface Props {
    labeledAbst: abstLabelPair[];
    isLimitedLength: boolean;
}
const props = defineProps<Props>();
const displayLabeledAbstInit: abstLabelPair[] = []
const displayLabeledAbst = ref(displayLabeledAbstInit);
const isDisplayFull = ref(false);

const updateDisplayLabeledAbst = (newVal: abstLabelPair[]) => {
  if (props.isLimitedLength && !isDisplayFull.value) {
    const maxLength = 200;
    let lengthAbst = 0;
    let tempArr: abstLabelPair[] = [];
    for (let i = 0; i < newVal.length; i++) {
      lengthAbst += newVal[i][0].length;
      tempArr.push(newVal[i]);
      if (lengthAbst > maxLength) {
        break;
      }
    }
    displayLabeledAbst.value = [...tempArr, [" ... ", ""]];
  } else {
    displayLabeledAbst.value = newVal;
  }
};

watch(() => props.labeledAbst, (newVal) => {
  updateDisplayLabeledAbst(newVal);
}, { immediate: true });

const displayFull = () => {
    displayLabeledAbst.value = props.labeledAbst;
    isDisplayFull.value = true;
}

</script>

<template>
    <template v-for="abstLabel in displayLabeledAbst" :key="abstLabel[0]">
        <span v-bind:class="abstLabel[1]" class="label">{{ abstLabel[0] }}</span>&nbsp;
    </template>
    <div v-if="props.isLimitedLength && !isDisplayFull">
        <a @click.prevent.stop="displayFull()" class="text-blue-500 hover:underline" href="#">Display full</a>
    </div>
</template>

<style scoped>


</style>