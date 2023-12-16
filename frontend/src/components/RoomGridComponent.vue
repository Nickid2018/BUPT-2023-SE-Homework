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

// ---- test function
// function supplyRoomDataTest(csrfToken: string, successCallback: (data: any) => void, errorCallback: (errorCode: number) => void) {
//   successCallback([
//     "1-114", "1-115", "1-116", "1-117", "1-118", "1-119", "1-120", "1-121", "1-122", "1-123", "1-124", "1-125", "1-126", "1-127", "1-128", "1-129", "1-130", "1-131", "1-132", "1-133", "1-134", "1-135", "1-136", "1-137", "1-138", "1-139", "1-140", "1-141", "1-142", "1-143", "1-144", "1-145", "1-146", "1-147", "1-148", "1-149", "1-150", "1-151", "1-152", "1-153", "1-154", "1-155", "1-156", "1-157", "1-158", "1-159", "1-160", "1-161", "1-162", "1-163", "1-164", "1-165", "1-166", "1-167", "1-168", "1-169", "1-170", "1-171", "1-172", "1-173", "1-174", "1-175", "1-176", "1-177", "1-178", "1-179", "1-180", "1-181", "1-182", "1-183", "1-184", "1-185", "1-186", "1-187", "1-188", "1-189", "1-190", "1-191", "1-192", "1-193", "1-194", "1-195", "1-196", "1-197", "1-198", "1-199", "1-200", "1-201", "1-202", "1-203", "1-204", "1-205", "1-206", "1-207", "1-208", "1-209", "1-210", "1-211", "1-212", "1-213", "1-214",
//   ]);
//   errorCallback;
//   csrfToken;
//   getAvailableDevices;
// }

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
  intervalId = setInterval(updateRoomData, 5000);
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