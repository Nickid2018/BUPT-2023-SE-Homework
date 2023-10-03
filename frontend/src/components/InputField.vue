<script setup lang="ts">
import {ref} from "vue";

defineProps<{
  placeholder?: string
  password?: boolean
  lineHeight?: string
  fontSize?: string
  error?: boolean
  id?: string
}>()

defineEmits<{
  (event: 'value-change', value: string): void,
  (event: 'focus-in'): void
}>()

const value = ref("");
const focused = ref(false);
</script>

<template>
  <div
      class="inline-flex items-center justify-center cursor-text px-[11px] py-[1px] rounded-md border-2 border-gray-300"
      :class="{'border-primary-500': focused, 'border-red-200': error}"
  >
    <input v-model="value"
           class="outline-none border-none p-0 bg-none w-full flex-grow"
           :style="{
               'line-height': lineHeight ? lineHeight : '1em',
               'font-size': fontSize ? fontSize : '1em'
           }"
           :id="id"
           :placeholder="placeholder"
           :type="password ? 'password' : 'text'"
           autocomplete="off"
           @change="$emit('value-change', value)"
           @focusin="focused = true; $emit('focus-in')"
           @focusout="focused = false"
    />
  </div>
</template>