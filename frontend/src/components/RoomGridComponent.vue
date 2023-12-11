<script setup lang="ts">
import {Ref, ref} from "vue";
import {getAvailableDevices, getAvailableDevicesWithOpen} from "../utils/protocol.ts";

const props = defineProps<{
  loginCsrfToken: string,
  displayMode: string
}>()

const emit = defineEmits<{
  (event: 'room-data-update', data: { [key: string]: any }): void,
  (event: 'select-room', data: string): void
}>()

const displayModeFunction: {
  [key: string]: (csrfToken: string, successCallback: (data: any) => void, errorCallback: (errorCode: number) => void) => void
} = {
  "checkout": getAvailableDevices,
  "admin": getAvailableDevicesWithOpen,
  "test": supplyRoomDataTest
}

const roomDataList = ref({}) as Ref<{ [key: string]: any }>

// ---- test function
function supplyRoomDataTest(csrfToken: string, successCallback: (data: any) => void, errorCallback: (errorCode: number) => void) {
  successCallback([
    "1-114",
    "1-115",
    "1-116",
    "2-223",
    "2-224",
    "2-233",
  ]);
}

// ----

function updateRoomData() {
  displayModeFunction[props.displayMode](props.loginCsrfToken, data => {
    roomDataList.value = data;
    emit('room-data-update', data);
    console.log(data)
  }, errorCode => {
    console.log(errorCode);
  })
}

updateRoomData();
setInterval(updateRoomData, 5000);

</script>

<template>
  <div class="flex flex-wrap gap-5 h-full p-5">
    <div v-for="data in roomDataList" :key="data" class="
          rounded-md drop-shadow-xl shadow-gray-200 bg-neutral-50 cursor-pointer
          hover:bg-primary-100 hover:shadow-primary-100 transition-all duration-150
      ">
      <div class="flex flex-col items-center justify-center m-4">
        <div class="text-xl" @click="$emit('select-room', displayMode == 'admin' ? data.room : data)">
          {{ displayMode == 'admin' ? data.room : data }}
        </div>
      </div>
    </div>
  </div>
</template>