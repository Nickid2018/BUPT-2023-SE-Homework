<script setup lang="ts">
import {onMounted, onUnmounted, Ref, ref} from "vue";
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
  "admin": supplyRoomDataTest,
}

const roomDataList = ref({}) as Ref<{ [key: string]: any }>

// ---- test function
function supplyRoomDataTest(csrfToken: string, successCallback: (data: any) => void, errorCallback: (errorCode: number) => void) {
  successCallback([
    {"room": "1-114", "is_on": true},
    {"room": "1-114", "is_on": false},
    {"room": "1-114", "is_on": false},
    {"room": "1-114", "is_on": false},
    {"room": "1-114", "is_on": true},
    {"room": "1-114", "is_on": false},
    {"room": "1-114", "is_on": true},
    {"room": "1-114", "is_on": false},
  ]);
  errorCallback;
  csrfToken;
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

let intervalId = 0;

onMounted(() => {
  updateRoomData();
  intervalId = setInterval(updateRoomData, 5000);
});

onUnmounted(() => {
  clearInterval(intervalId);
});

</script>

<template>
  <div class="overflow-y-scroll">
    <div class="flex flex-wrap gap-5 p-5">
      <div v-for="data in roomDataList" :key="data" class="
          rounded-md drop-shadow-xl shadow-gray-200 bg-neutral-50 cursor-pointer
          hover:bg-primary-100 hover:shadow-primary-100 transition-all duration-150
          shrink-0 min-w-[18%]
      " @click="$emit('select-room', displayMode == 'admin' ? data.room : data)">
        <div class="align-middle m-4">
          <div class="text-xl text-center select-none">
            {{ displayMode == 'admin' ? data.room : data }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>