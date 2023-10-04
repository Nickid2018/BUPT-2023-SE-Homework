<script setup lang="ts">
import {SYSTEM_NAME, UNLOGIN} from "./shared-constants.ts";

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
  <div class="flex h-full fixed flex-col bg-primary-100">
    <div class="flex-none mx-10 my-5">
      {{ SYSTEM_NAME }}
    </div>
    <div class="flex-auto flex flex-col border-t-2 border-t-gray-400">
      <div v-for="(panel, index) in (loginState ? availablePanelsLogin : availablePanelsUnLogin)"
           :key="index"
           class="flex-none mx-10 my-5"
           :class="{'text-primary-500': nowSelected !== index}"
           @click="nowSelected = index"
      >
        {{ panel }}
      </div>
    </div>
    <div class="flex-none mx-10 my-5">
      <div v-if="loginState" @click="logoutNow">
        {{ loginName }}
      </div>
      <div v-if="!loginState" @click="loginPanel = true">
        {{ UNLOGIN }}
      </div>
    </div>
  </div>
  <LoginPanel v-if="loginPanel" @close="loginPanel = false" @login="(ln: string, csrf: string) => {
    loginState = true;
    loginName = ln;
    loginCsrfToken = csrf;
  }"/>
</template>
