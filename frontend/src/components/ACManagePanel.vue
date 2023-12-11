<script setup lang="ts">
import RoomGridComponent from "./RoomGridComponent.vue";
import {ref} from "vue";

defineProps<{
  loginCsrfToken: string
}>()

const selectedRoom = ref("");

</script>

<template>
  <RoomGridComponent class="h-[50vh]" :login-csrf-token="loginCsrfToken" display-mode="admin"
                     @select-room="data => selectedRoom = data"/>
</template>