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
  "admin": getAvailableDevicesWithOpen,
}

const roomDataList = ref({}) as Ref<{ [key: string]: any }>;

function getCurrentTime() {
  return new Date().toLocaleString();
}

const lastUpdateTime = ref(getCurrentTime());

// ----

function updateRoomData() {
  displayModeFunction[props.displayMode](props.loginCsrfToken, data => {
    roomDataList.value = data;
    lastUpdateTime.value = getCurrentTime();
    emit('room-data-update', data);
  }, errorCode => {
    console.log(errorCode);
  })
}

let intervalId = 0;

onMounted(() => {
  updateRoomData();
  intervalId = setInterval(updateRoomData, 1000);
});

onUnmounted(() => {
  clearInterval(intervalId);
});

</script>

<template>
  <div class="overflow-y-scroll">
    <div class="flex flex-wrap gap-5 p-5">
      <div v-for="data in roomDataList" :key="data"
           class="
                  rounded-md drop-shadow-xl bg-neutral-50 cursor-pointer
                  transition-all duration-150 shrink-0 min-w-[18%]
                 "
           :class="{
                'border-2 border-green-200 shadow-green-200 hover:bg-green-50': displayMode == 'admin' && data.is_on,
                'border-2 border-red-100 shadow-red-200 hover:bg-red-50': displayMode == 'admin' && !data.is_on,
                'shadow-gray-200 hover:bg-primary-100 hover:shadow-primary-100': displayMode != 'admin'
           }"
           @click="$emit('select-room', displayMode == 'admin' ? data.room : data)"
      >
        <div class="align-middle m-4">
          <div class="text-xl text-center select-none">
            {{ displayMode == 'admin' ? data.room : data }}
          </div>
        </div>
      </div>
    </div>
    <div class="text-right right-0 bottom-0 z-10 text-gray-300 italic text-sm">
      最后更新于 {{ lastUpdateTime }}
    </div>
  </div>
</template>