
<script setup lang="ts">
/**
 * ページをスクロールすると、ページトップに戻るボタンを表示する Component
 * 
 * Props: None
 *
 * Emits: None
 */
import { ref, onMounted, onUnmounted } from 'vue';


const isVisible = ref(false);

const checkScroll = () => {
    if (window.scrollY > 200) {
        isVisible.value = true;
    } else {
        isVisible.value = false;
    }
};

const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
};

onMounted(() => {
    window.addEventListener('scroll', checkScroll);
});

onUnmounted(() => {
    window.removeEventListener('scroll', checkScroll);
});

</script>

<template>
    <button v-if="isVisible" @click="scrollToTop"
        class="back-to-top bg-gray-600 hover:bg-gray-500 text-white rounded px-4 py-2">
        ↑Page top
    </button>
</template>

<style>
.back-to-top {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    border: none;
    cursor: pointer;
    border-radius: 5px;
    z-index: 1000;
}
</style>
