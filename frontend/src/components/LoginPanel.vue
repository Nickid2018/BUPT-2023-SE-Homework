<script setup lang="ts">
import {LOGIN} from "../shared-constants.ts";
import InputField from "./InputField.vue";
import {ref} from "vue";

defineEmits<{
  (event: 'close'): void,
  (event: 'login', loginName: string): void
}>()

const username = ref("");
const password = ref("");

</script>

<template>
  <div class="z-10 bg-opacity-40 bg-black fixed h-full w-full flex justify-center items-center">
    <div class="bg-white rounded-md w-fit h-fit px-10 py-5 flex flex-col items-center">
      <div class="font-bold my-5 flex-none text-2xl">
        {{LOGIN}}
      </div>
      <div class="flex-1 my-2">
        <label class="mr-3" for="username">用户名</label>
        <InputField @value-change="value => username = value"/>
      </div>
      <div class="flex-1 my-2">
        <label class="mr-3" for="username">密码</label>
        <InputField :password=true @value-change="value => password = value"/>
      </div>
    </div>
  </div>
</template>