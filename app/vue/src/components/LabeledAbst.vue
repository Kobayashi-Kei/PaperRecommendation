<script setup lang="ts">
import { defineProps } from "vue";
import type { abstLabelPair, labelScoreOfSimilarity } from '@/type'

interface Props {
    labeledAbst: abstLabelPair[];
}
const props = defineProps<Props>();

</script>

<template>
    <template v-for="abstLabel in props.labeledAbst" :key="abstLabel[0]">
        <span v-bind:class="abstLabel[1]" class="label">{{ abstLabel[0] }}</span>&nbsp;
    </template>
</template>

<style scoped>


</style>