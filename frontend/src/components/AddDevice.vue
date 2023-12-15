<script setup lang="ts">
import { ref, defineEmits } from 'vue';

defineProps<{
  roomPlaceholder?: string;
  keyPlaceholder?: string;
}>()

const roomValue = ref("");
const keyInputValue = ref("");
const roomInputFocused = ref(false);
const keyInputFocused = ref(false);

const emit = defineEmits<{
  (event: 'confirm', roomValue: string, keyInputValue: string): void;
  (event: 'close-modal'): void;
}>()

const confirm = () => {
  emit('confirm', roomValue.value, keyInputValue.value);
  closeModal();
};

const closeModal = () => {
  emit('close-modal');
};
</script>

<template>
  <div class="fixed top-0 left-0 right-0 bottom-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
    <div class="bg-white p-8 rounded-md">
      <h2 class="text-2xl font-bold mb-8">添加设备</h2>

      <!-- Room Input -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700">房间号</label>
        <div
          class="inline-flex items-center justify-center cursor-text px-[11px] py-[1px] rounded-md border-2 border-gray-300"
          :class="{'border-primary-500': roomInputFocused}"
        >
          <input
            v-model="roomValue"
            @focus="roomInputFocused = true"
            @blur="roomInputFocused = false"
            class="outline-none border-none p-0 bg-none w-full flex-grow"
            type="text"
            :placeholder="roomPlaceholder || '请输入房间号'"
          />
        </div>
      </div>

      <!-- Key Input -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700">Key</label>
        <div
          class="inline-flex items-center justify-center cursor-text px-[11px] py-[1px] rounded-md border-2 border-gray-300"
          :class="{'border-primary-500': keyInputFocused}"
        >
          <input
            v-model="keyInputValue"
            @focus="keyInputFocused = true"
            @blur="keyInputFocused = false"
            class="outline-none border-none p-0 bg-none w-full"
            type="text"
            :placeholder="keyPlaceholder || '请输入Key'"
          />
        </div>
      </div>

      <div class="flex justify-center mt-8 mb-2">
        <!-- Confirm Button -->
        <button
            @click="confirm"
            class="bg-blue-300 hover:bg-blue-400 text-white font-bold py-2 px-6 rounded"
        >
            确认
        </button>

        <!-- Close Modal Button -->
        <button
            @click="closeModal"
            class="bg-gray-100 hover:bg-gray-200 text-gray-600 font-bold py-2 px-6 rounded ml-4"
        >
            关闭
        </button>
      </div>
    </div>
  </div>
</template>