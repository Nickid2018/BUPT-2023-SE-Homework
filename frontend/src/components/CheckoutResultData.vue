<script setup lang="ts">
import {DeviceData} from "../utils/protocol.ts";
import {ElTable, ElTableColumn} from 'element-plus';

const props = defineProps<{
  data: DeviceData[]
}>()

const emit = defineEmits<{
  (event: 'close'): void
}>()

</script>

<template>
  <div class="z-20 bg-opacity-40 top-0 left-0 bg-black fixed h-full w-full flex justify-center items-center">
    <div class="bg-white rounded-md w-fit h-fit px-10 py-5 flex flex-col items-center">
      <div class="text-2xl font-bold py-4">
        退房账单
      </div>
      <div class="flex">
        <div>
          <el-table :data="props.data" class="max-w-[33vw] py-4">
            <el-table-column prop="start_time" label="开始时间" width="200"/>
            <el-table-column prop="end_time" label="结束时间" width="200"/>
            <el-table-column prop="temperature" label="温度" width="75"/>
            <el-table-column prop="wind_speed" label="风速" width="75"/>
            <el-table-column prop="mode" label="模式" width="75"/>
            <el-table-column prop="sweep" label="扫风" width="75"/>
            <el-table-column prop="duration" label="时长" width="75"/>
            <el-table-column prop="cost" label="费用" fixed="right"/>
          </el-table>
        </div>
      </div>
      <div>
        <button class="rounded-md px-4 py-2 bg-primary-100 " @click="emit('close')">
          退房完成
        </button>
      </div>
    </div>
  </div>
</template>