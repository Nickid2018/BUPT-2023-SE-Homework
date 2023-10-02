<script setup lang="ts">
import {ref} from "vue";

defineProps<{
  placeholder?: string
  password?: boolean
}>()

defineEmits<{
  (event: 'value-change', value: string): void
}>()

const value = ref("");
const focused = ref(false);
</script>

<template>
  <div
      class="inline-flex items-center justify-center cursor-text px-[11px] py-[1px] rounded-md border-2 border-gray-300"
      :class="{'border-primary-500': focused}"
  >
    <input v-model="value"
           class="outline-none border-none p-0 bg-none w-full flex-grow leading-[10px]"
           :placeholder="placeholder"
           :type="password ? 'password' : 'text'"
           autocomplete="off"
           @change="$emit('value-change', value)"
           @focusin="focused = true"
           @focusout="focused = false"
    />
  </div>
</template>