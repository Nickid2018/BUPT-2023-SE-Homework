<script setup lang="ts">
import RoomGridComponent from "./RoomGridComponent.vue";

defineProps<{
  loginCsrfToken: string
}>()

</script>

<template>
  <div>
    <RoomGridComponent :login-csrf-token="loginCsrfToken" display-mode="test"/>
  </div>
</template>