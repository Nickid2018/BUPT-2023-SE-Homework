<script setup lang="ts">
import {ESCAPE, LOGIN, PASSWORD, USERNAME} from "../shared-constants.ts";
import {ERROR_CODE_MAP, login} from "../utils/protocol.ts";
import InputField from "./InputField.vue";
import {ref} from "vue";

const emit = defineEmits<{
  (event: 'close'): void,
  (event: 'login', loginName: string): void
}>()

const username = ref("");
const password = ref("");
const errorMessage = ref("");

function loginNow() {
  login(username.value, password.value, (data) => {
    emit('login', data.username);
    emit('close');
  }, errorCode => {
    errorMessage.value = ERROR_CODE_MAP[errorCode];
    console.log(errorCode)
  });
}
</script>

<template>
  <div class="z-10 bg-opacity-40 bg-black fixed h-full w-full flex justify-center items-center">
    <div class="bg-white rounded-md w-fit h-fit px-10 py-5 flex flex-col items-center">
      <div class="font-bold my-5 flex-none text-2xl">
        {{ LOGIN }}
      </div>
      <div class="flex-none flex flex-col items-end">
        <div class="flex-1 my-2">
          <label class="mr-3" for="username">{{ USERNAME }}</label>
          <InputField font-size="1em" line-height="2em" :error="errorMessage !== ''" id="username"
                      @value-change="value => username = value" @focus-in="errorMessage = ''"/>
        </div>
        <div class="flex-1 my-2">
          <label class="mr-3" for="password">{{ PASSWORD }}</label>
          <InputField font-size="1em" line-height="2em" :password=true :error="errorMessage !== ''" id="password"
                      @value-change="value => password = value" @focus-in="errorMessage = ''"/>
        </div>
        <div v-if="errorMessage !== ''" class="flex-none mb-2 text-red-500 text-[80%]">
          {{ errorMessage }}
        </div>
      </div>
      <div class="flex-none flex items-center gap-10 mt-2 px-10 py-2 w-full">
        <button class="flex-1 bg-primary-500 rounded-md py-2" @click="loginNow">
          {{ LOGIN }}
        </button>
        <button class="flex-1 bg-primary-500 rounded-md py-2" @click="$emit('close')">
          {{ ESCAPE }}
        </button>
      </div>
    </div>
  </div>
</template>