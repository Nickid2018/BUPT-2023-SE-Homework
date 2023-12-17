<script setup lang="ts">
import {ref, defineEmits} from 'vue';
import InputField from "./InputField.vue";

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
};

const closeModal = () => {
  emit('close-modal');
};
</script>

<template>
  <div class="fixed top-0 left-0 right-0 bottom-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
    <div class="bg-white rounded-md w-fit h-fit px-10 py-5 flex flex-col items-center">
      <div class="flex-none text-2xl font-bold mb-8">添加设备</div>

      <div class="flex-none flex flex-col items-end">
        <!-- Room Input -->
        <div class="flex-1 my-3">
          <label class="mr-3">房间号</label>
          <InputField font-size="1em" line-height="2em" :error="false" id="roomValue"
                      @value-change="value => roomValue = value"/>
        </div>

        <!-- Key Input -->
        <div class="flex-1 my-3">
          <label class="mr-3">公钥</label>
          <InputField font-size="1em" line-height="2em" :error="false" id="keyInputValue"
                      @value-change="value => keyInputValue = value"/>
        </div>
      </div>

      <div class="flex-none flex items-center gap-10 mt-2 px-10 py-2 w-full">
        <!-- Confirm Button -->
        <button
            @click="confirm"
            class="bg-blue-300 hover:bg-blue-400 text-white font-bold py-2 px-6 rounded flex-1"
        >
          确认
        </button>

        <!-- Close Modal Button -->
        <button
            @click="closeModal"
            class="bg-gray-100 hover:bg-gray-200 text-gray-600 font-bold py-2 px-6 rounded ml-4 flex-1"
        >
          关闭
        </button>
      </div>
    </div>
  </div>
</template>