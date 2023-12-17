<script setup lang="ts">
import {DeviceData} from "../utils/protocol.ts";
import {ElTable, ElTableColumn} from 'element-plus';
import {ref} from "vue";

const props = defineProps<{
  total_cost: number,
  total_duration: number,
  data: DeviceData[]
}>()

const emit = defineEmits<{
  (event: 'close'): void
}>()

const showDetail = ref(false);


function printDetails() {
  // const items = billDetails;
  const items = billDetails.value;
  const header = [
    'start_time',
    'end_time',
    'temperature',
    'wind_speed',
    'mode',
    'sweep',
    'duration',
    'cost'
  ];
  const replacer = (_: any, value: any) => {
    if (typeof value === 'boolean') {
      return value ? 'Yes' : 'No';
    }
    return value === null ? '' : value;
  };
  const csv = [
    header.join(','),
    ...items.map((row: any) => header.map(fieldName => JSON.stringify(row[fieldName], replacer)).join(','))
  ].join('\r\n');
  const blob = new Blob([csv], { type: 'text/csv' });
  const link = document.createElement('a');
  link.href = window.URL.createObjectURL(blob);
  link.download = 'bill_details.csv';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

</script>

<template>
  <div class="z-20 bg-opacity-40 top-0 left-0 bg-black fixed h-full w-full flex justify-center items-center">
    <div class="bg-white rounded-md w-fit h-fit px-10 py-5 flex flex-col items-center min-w-[40vw]">
      <div class="text-2xl font-bold py-4">
        退房账单
      </div>
      <div class="flex" v-if="showDetail">
        <div>
          <el-table :data="props.data" max-height="50vh" class="max-w-[50vw] my-4">
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
      <div v-else class="flex flex-col">
        <div class="m-2">本次空调使用时长：{{ props.total_duration }} 秒</div>
        <div class="m-2">本次空调使用消费：{{ props.total_cost }} 元</div>
      </div>
      <div class="flex gap-10 mt-6">
        <button class="rounded-md px-4 py-2 bg-primary-100 " @click="showDetail = !showDetail">
          {{showDetail ? '隐藏' : '显示'}}详单
        </button>
        <button class="rounded-md px-4 py-2 bg-primary-100 " v-if="showDetail" @click="printDetails">
          导出详单
        </button>
        <button class="rounded-md px-4 py-2 bg-primary-100 " @click="emit('close')">
          退房完成
        </button>
      </div>
    </div>
  </div>
</template>