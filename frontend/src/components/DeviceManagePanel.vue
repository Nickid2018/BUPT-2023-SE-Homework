<script setup lang="ts">
import RoomGridComponent from "./RoomGridComponent.vue";
import {ref} from "vue";
import AddDevice from "./AddDevice.vue";
import CancelDevice from "./CancelDevice.vue";

defineProps<{
  loginCsrfToken: string
}>()

const emit = defineEmits<{
  (event: 'close'): void;
}>()

const selectedRoom = ref("");
const isAddDeviceOpen = ref(false);
const isCancelDeviceOpen = ref(false);

const openAddDevice = () => {
  isAddDeviceOpen.value = true;
};
const closeAddDevice = () => {
  isAddDeviceOpen.value = false;
};

const openCancelDevice = () => {
  isCancelDeviceOpen.value = true;
};
const closeCancelDevice = () => {
  isCancelDeviceOpen.value = false;
};

</script>

<template>
  <RoomGridComponent class="h-[50vh]" :login-csrf-token="loginCsrfToken" display-mode="checkout"
                     @select-room="data => selectedRoom = data"/>

  <div class="flex justify-center mt-24">
    <button @click="openAddDevice" class="bg-blue-300 hover:bg-blue-400 text-white font-bold py-2 px-12 rounded mt-4">
      添加设备
    </button>
    <button @click="openCancelDevice" class="bg-red-300 hover:bg-red-400 text-white font-bold py-2 px-12 rounded mt-4 ml-24">
      取消设备
    </button>
  </div>
  <AddDevice v-if="isAddDeviceOpen" @close-modal="closeAddDevice" />
  <CancelDevice v-if="isCancelDeviceOpen" @close-modal="closeCancelDevice" />
                    
</template>