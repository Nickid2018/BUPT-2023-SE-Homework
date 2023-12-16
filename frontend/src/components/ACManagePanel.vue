<script setup lang="ts">
import RoomGridComponent from "./RoomGridComponent.vue";
import {onMounted, onUnmounted, ref} from "vue";
import {getRoomStatus, operationDevice} from "../utils/protocol.ts";

const props = defineProps<{
  loginCsrfToken: string
}>()

const MODE_NAME_MAP: {
  [key: string]: string
} = {
  "cool": "制冷",
  "hot": "制热",
  "wind": "送风"
};

const MODE_COLOR: {
  [key: string]: string
} = {
  "cool": "text-blue-500",
  "hot": "text-red-500",
  "wind": "text-green-500"
};

const selectedRoom = ref("");
const selectRoomData = ref({
  is_on: true,
  temperature: 26,
  wind_speed: 0,
  mode: "cool",
  sweep: false,
  last_update: ""
});

function updateSelectRoomDataAndThen(selectRoom: string) {
  selectedRoom.value = selectRoom;
  getRoomStatus(props.loginCsrfToken, selectRoom, data => {
    selectRoomData.value = data;
    if (targetTemperature.value === selectRoomData.value.temperature)
      temperatureDataSet.value = false;
    if (targetWindSpeed.value === selectRoomData.value.wind_speed)
      windSpeedDataSet.value = false;
    if (modeList[targetModeIndex.value] === selectRoomData.value.mode)
      modeDataSet.value = false;

    targetTemperature.value = selectRoomData.value.temperature;
    targetWindSpeed.value = selectRoomData.value.wind_speed;

    temperatureDataSet.value = false;
    windSpeedDataSet.value = false;

    targetModeIndex.value = modeList.indexOf(selectRoomData.value.mode);
    modeDataSet.value = false;

    targetSweep.value = selectRoomData.value.sweep;
  }, errorCode => {
    console.log(errorCode);
  });
}

// 16-35
function getTemperatureColor(temperature: number) {
  if (temperature < 16) return 240;
  if (temperature > 35) return 0;
  return 240 - (temperature - 16) / 20 * 240;
}

// ---- Control ----
function control(operation: string, data: any) {
  operationDevice(props.loginCsrfToken, selectedRoom.value, operation, data, () => {
    updateSelectRoomDataAndThen(selectedRoom.value);
  }, errorCode => {
    console.log(errorCode);
  });
}

function togglePower() {
  if (selectRoomData.value.is_on)
    control("stop", "");
  else
    control("start", "");
}

const targetTemperature = ref(26);
const temperatureDataSet = ref(false);

function sendTemperature() {
  if (targetTemperature.value !== selectRoomData.value.temperature) {
    control("temperature", targetTemperature.value);
    temperatureDataSet.value = true;
  }
}

const targetWindSpeed = ref(0);
const windSpeedDataSet = ref(false);

function sendWindSpeed() {
  if (targetWindSpeed.value !== selectRoomData.value.wind_speed) {
    control("wind_speed", targetWindSpeed.value);
    windSpeedDataSet.value = true;
  }
}

const modeList = ["cool", "hot", "wind"];

const targetModeIndex = ref(0);
const modeDataSet = ref(false);

function sendMode() {
  if (modeList[targetModeIndex.value] !== selectRoomData.value.mode) {
    control("mode", modeList[targetModeIndex.value]);
    modeDataSet.value = true;
  }
}

const targetSweep = ref(false);

function toggleSweep() {
  targetSweep.value = !selectRoomData.value.sweep;
  control("sweep", targetSweep.value);
}
// -----------------

// ---- Interval ----
let intervalId = 0;

onMounted(() => intervalId = setInterval(() => {
  if (selectedRoom.value !== "")
    updateSelectRoomDataAndThen(selectedRoom.value);
}, 5000));

onUnmounted(() => clearInterval(intervalId));

// ------------------

function selectRoom(room: string) {
  if (selectedRoom.value === room) return;

  selectedRoom.value = room;

  updateSelectRoomDataAndThen(room);
}

</script>

<template>
  <RoomGridComponent class="h-[40vh] my-2 border-y-2 border-y-neutral-100" :login-csrf-token="loginCsrfToken"
                     display-mode="admin" @select-room="selectRoom"/>
  <div class="flex-none w-full h-[calc(60vh-120px)] flex" v-if="selectedRoom !== ''">
    <div class="flex-none w-fit m-5 pr-20 flex flex-col justify-center border-r-2 border-neutral-100">
      <div class="inline-flex align-bottom">
        <img src="/svg/house.svg" alt="house" class="h-8 w-8"/>
        <span class="text-xl">房间</span>
      </div>
      <div class="text-3xl font-bold">{{ selectedRoom }}</div>
    </div>
    <div class="flex-auto py-5 pr-5 pl-20 grid grid-cols-3 grid-rows-2">
      <div class="flex">
        <div class="flex-1 flex flex-col justify-center">
          <div class="inline-flex">
            <img src="/svg/power.svg" alt="temperature" class="h-8 w-8"/>
            <span class="text-xl ml-2">状态</span>
          </div>
          <div
              class="p-2 text-5xl font-bold cursor-pointer select-none"
              :class="{
                'text-green-500': selectRoomData.is_on,
                'text-red-400': !selectRoomData.is_on
              }"
              @click="togglePower"
          >
            {{ selectRoomData.is_on ? "工作中" : "未开启" }}
          </div>
        </div>
        <div class="flex-1">
        </div>
      </div>
      <div class="flex">
        <div class="flex-1 flex flex-col justify-center">
          <div class="inline-flex">
            <img src="/svg/temperature.svg" alt="temperature" class="h-8 w-8"/>
            <span class="text-xl ml-2">温度</span>
          </div>
          <div
              v-if="selectRoomData.is_on"
              class="p-2 text-5xl font-bold cursor-pointer select-none"
              :style="{
                'color': `hsl(${getTemperatureColor(selectRoomData.temperature)}, 50%, 50%)`
              }"
              @wheel="event => {
                if (!temperatureDataSet)
                  targetTemperature = Math.floor(Math.min(Math.max(targetTemperature - event.deltaY / 100, 16), 35));
              }"
              @click="sendTemperature"
          >
            {{ selectRoomData.temperature }}℃
          </div>
          <div
              v-else
              class="p-2 text-5xl font-bold"
          >
            -
          </div>
        </div>
        <div class="flex-1 flex items-center">
          <div
              v-if="targetTemperature != selectRoomData.temperature && selectRoomData.is_on"
              class="text-neutral-500 text-xl"
              style="transform: skewX(-15deg)"
          >
            {{ temperatureDataSet ? "正在" : "即将" }}设定为 {{ targetTemperature }}℃
          </div>
        </div>
      </div>
      <div class="flex">
        <div class="flex-1 flex flex-col justify-center">
          <div class="inline-flex">
            <img src="/svg/fan.svg" alt="fan" class="h-8 w-8"/>
            <span class="text-xl ml-2">风速</span>
          </div>
          <div
              v-if="selectRoomData.is_on"
              class="p-2 text-5xl font-bold cursor-pointer select-none"
              @wheel="event => {
                if (!windSpeedDataSet)
                  targetWindSpeed = Math.floor(Math.min(Math.max(targetWindSpeed - event.deltaY / 100, 1), 3));
              }"
              @click="sendWindSpeed"
          >
            {{ selectRoomData.wind_speed }} 档
          </div>
          <div
              v-else
              class="p-2 text-5xl font-bold"
          >
            -
          </div>
        </div>
        <div class="flex-1 flex items-center">
          <div
              v-if="targetWindSpeed != selectRoomData.wind_speed && selectRoomData.is_on"
              class="text-neutral-500 text-xl"
              style="transform: skewX(-15deg)"
          >
            {{ windSpeedDataSet ? "正在" : "即将" }}设定为 {{ targetWindSpeed }} 档
          </div>
        </div>
      </div>
      <div class="flex">
        <div class="flex-1 flex flex-col justify-center">
          <div class="inline-flex">
            <img src="/svg/mode.svg" alt="fan" class="h-8 w-8"/>
            <span class="text-xl ml-2">模式</span>
          </div>
          <div
              v-if="selectRoomData.is_on"
              class="p-2 text-5xl font-bold cursor-pointer select-none"
              :class="MODE_COLOR[selectRoomData.mode]"
              @wheel="event => {
                if (!modeDataSet)
                  targetModeIndex = Math.floor(Math.min(Math.max(targetModeIndex - event.deltaY / 100, 0), 2));
              }"
              @click="sendMode"
          >
            {{ MODE_NAME_MAP[selectRoomData.mode] }}
          </div>
          <div
              v-else
              class="p-2 text-5xl font-bold"
          >
            -
          </div>
        </div>
        <div class="flex-1 flex items-center">
          <div
              v-if="modeList[targetModeIndex] != selectRoomData.mode && selectRoomData.is_on"
              class="text-neutral-500 text-xl"
              style="transform: skewX(-15deg)"
          >
            {{ modeDataSet ? "正在" : "即将" }}设定为{{ MODE_NAME_MAP[modeList[targetModeIndex]] }}模式
          </div>
        </div>
      </div>
      <div class="flex">
        <div class="flex-1 flex flex-col justify-center">
          <div class="inline-flex">
            <img src="/svg/sweep.svg" alt="fan" class="h-8 w-8"/>
            <span class="text-xl ml-2">扫风</span>
          </div>
          <div
              v-if="selectRoomData.is_on"
              class="p-2 text-5xl font-bold cursor-pointer select-none"
              :class="{
                'text-green-500': selectRoomData.sweep,
                'text-red-400': !selectRoomData.sweep
              }"
              @click="toggleSweep"
          >
            {{ selectRoomData.sweep ? "开启" : "关闭" }}
          </div>
          <div
              v-else
              class="p-2 text-5xl font-bold"
          >
            -
          </div>
        </div>
        <div class="flex-1 flex items-center">
          <div
              v-if="targetSweep != selectRoomData.sweep && selectRoomData.is_on"
              class="text-neutral-500 text-xl"
              style="transform: skewX(-15deg)"
          >
            正在{{ targetSweep ? "开启" : "关闭" }}扫风
          </div>
        </div>
      </div>
    </div>
  </div>
</template>