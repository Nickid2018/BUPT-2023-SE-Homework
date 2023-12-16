<script setup lang="ts">
import RoomGridComponent from "./RoomGridComponent.vue";
import {ref} from "vue";
import {checkInRoom, checkOutRoom, DeviceData} from "../utils/protocol.ts";
import CheckoutResultData from "./CheckoutResultData.vue";

const props = defineProps<{
  loginCsrfToken: string
}>()

const selectedRoom = ref("");
const checkedRooms = ref<string[]>([]);
const checkoutResultData = ref<DeviceData[]>([]);

function checkIn() {
  checkInRoom(props.loginCsrfToken, selectedRoom.value, () => {
    checkedRooms.value.push(selectedRoom.value);
  }, errorCode => {
    console.log(errorCode);
    checkedRooms.value.push(selectedRoom.value);
  });
}

function checkOut() {
  checkOutRoom(props.loginCsrfToken, selectedRoom.value, data => {
    console.log(data)
    checkoutResultData.value = data.report.details;
    checkedRooms.value = checkedRooms.value.filter(room => room !== selectedRoom.value);
  }, errorCode => {
    console.log(errorCode);
  });
}

</script>

<template>
  <RoomGridComponent class="h-[50vh]" :login-csrf-token="loginCsrfToken" display-mode="checkout"
                     @select-room="data => selectedRoom = data"/>
  <div class="flex-none w-full h-[calc(50vh-100px)] flex items-center" v-if="selectedRoom !== ''">
    <div class="flex-1 text-right py-5">
      <div class="mr-16">
        房间号
      </div>
      <div class="mr-16 font-bold text-2xl">
        {{ selectedRoom }}
      </div>
    </div>
    <div class="flex-1 flex flex-col items-start gap-8 border-l-2 border-neutral-300 py-5 h-fit">
      <button
          class="ml-16 rounded-md bg-primary-100 hover:bg-primary-300 transition-all duration-150 px-7 py-2"
          :disabled="checkedRooms.includes(selectedRoom)"
          @click="checkIn"
      >
        {{ checkedRooms.includes(selectedRoom) ? "已入住" : "入住" }}
      </button>
      <button
          class="ml-16 rounded-md bg-primary-100 hover:bg-primary-300 transition-all duration-150 px-7 py-2"
          :disabled="!checkedRooms.includes(selectedRoom)"
          @click="checkOut"
      >
        {{ !checkedRooms.includes(selectedRoom) ? "未入住" : "退房" }}
      </button>
    </div>
  </div>
  <CheckoutResultData v-if="checkoutResultData.length > 0" :data="checkoutResultData" @close="checkoutResultData = []"/>
</template>