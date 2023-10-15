<script setup lang="ts">
import {LOGIN, SYSTEM_NAME} from "./shared-constants.ts";

import {logout} from "./utils/protocol.ts";
import LoginPanel from "./components/LoginPanel.vue";
import {ref} from "vue";

// Ref definitions ---------------------
const loginState = ref(false);
const loginName = ref("");
const loginCsrfToken = ref("");
const nowSelected = ref(0);

const loginPanel = ref(false);
// -------------------------------------

// Panel definitions -------------------
const availablePanelsUnLogin = [
  "主页"
];

const availablePanelsLogin = [
  "主页",
  "入住/退房",
  "空调管理"
];

const iconMap = [
  "M240-200h120v-240h240v240h120v-360L480-740 240-560v360Zm-80 80v-480l320-240 320 240v480H520v-240h-80v240H160Zm320-350Z",
  "M440-440q17 0 28.5-11.5T480-480q0-17-11.5-28.5T440-520q-17 0-28.5 11.5T400-480q0 17 11.5 28.5T440-440ZM280-120v-80l240-40v-445q0-15-9-27t-23-14l-208-34v-80l220 36q44 8 72 41t28 77v512l-320 54Zm-160 0v-80h80v-560q0-34 23.5-57t56.5-23h400q34 0 57 23t23 57v560h80v80H120Zm160-80h400v-560H280v560Z",
  "M440-80v-166L310-118l-56-56 186-186v-80h-80L174-254l-56-56 128-130H80v-80h166L118-650l56-56 186 186h80v-80L254-786l56-56 130 128v-166h80v166l130-128 56 56-186 186v80h80l186-186 56 56-128 130h166v80H714l128 130-56 56-186-186h-80v80l186 186-56 56-130-128v166h-80Z"
];

// -------------------------------------

function logoutNow() {
  logout(loginCsrfToken.value, () => {
    loginState.value = false;
    loginName.value = "";
    loginCsrfToken.value = "";
    nowSelected.value = 0;
  }, errorCode => {
    console.log(errorCode);
  })
}

</script>

<template>
  <!-- Left Panel -->
  <div class="flex h-full fixed flex-col bg-white px-10">
    <div class="flex-none mx-10 my-10 flex font-bold text-xl">
      <span>{{ SYSTEM_NAME }}</span>
    </div>
    <div class="flex-auto flex flex-col border-t-[1px] border-t-gray-400 pt-5">
      <div v-for="(panel, index) in (loginState ? availablePanelsLogin : availablePanelsUnLogin)"
           :key="index"
           class="flex-none px-6 mx-4 py-2 my-3 flex transition-all duration-150 hover:text-neutral-300"
           :class="{
             'text-neutral-500': nowSelected !== index,
             '!text-white': nowSelected === index,
             'bg-primary-700': nowSelected === index,
             'rounded-md': nowSelected === index
           }"
           @click="nowSelected = index"
      >
        <svg height="24" width="24" viewBox="0 -960 960 960"
             class="mr-2 transition-all duration-150"
             :class="{'fill-neutral-500': nowSelected !== index, 'fill-white': nowSelected === index}">
          <path :d="iconMap[index]"/>
        </svg>
        <span class="cursor-pointer transition-all duration-150">{{ panel }}</span>
      </div>
    </div>
    <div class="flex-none mx-10 my-5">
      <div v-if="loginState" @click="logoutNow">
        {{ loginName }}
      </div>
      <div v-if="!loginState" class="flex" @click="loginPanel = true">
        <img src="/svg/login.svg" alt="login" class="mr-2"/>
        <span class="cursor-pointer">{{ LOGIN }}</span>
      </div>
    </div>
  </div>
  <LoginPanel v-if="loginPanel" @close="loginPanel = false" @login="(ln: string, csrf: string) => {
    loginState = true;
    loginName = ln;
    loginCsrfToken = csrf;
  }"/>
</template>
