<script setup lang="ts">
import { onMounted, watch } from 'vue';
import { $t } from '@/locales';
import { useAppStore } from '@/store/modules/app';
import { useEcharts } from '@/hooks/common/echarts';

defineOptions({
  name: 'LineChart'
});

const appStore = useAppStore();

const { domRef, updateOptions } = useEcharts(() => ({
  title: {
    text: '指标历史曲线图'
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross',
      label: {
        backgroundColor: '#6a7985'
      }
    }
  },
  legend: {
    data: ["测量值"]
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: [] as string[]
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      color: '#26deca',
      name: "测量值",
      type: 'line',
      smooth: true,
      // areaStyle: {
      //   color: {
      //     type: 'linear',
      //     x: 0,
      //     y: 0,
      //     x2: 0,
      //     y2: 1,
      //     colorStops: [
      //       {
      //         offset: 0.25,
      //         color: '#26deca'
      //       },
      //       {
      //         offset: 1,
      //         color: '#fff'
      //       }
      //     ]
      //   }
      // },
      emphasis: {
        focus: 'series'
      },
      data: [],
      markLine: {
        // silent: true, // 不触发鼠标事件  
        lineStyle: {
          color: '#ff0000'
        },
        label: {
          show: true,
          position: 'end'
        },
        data: [
          { yAxis: 8000, lineStyle: { color: '#ed2939' }, },
          { yAxis: 6000, lineStyle: { color: '#f5a623' } },
        ]
      },
    }
  ],
  dataZoom: [
    {
      type: 'inside',
      start: 0,
      end: 100
    },
    {
      start: 0,
      end: 100
    }
  ],
  visualMap: {
    show: false,
    top: 50,
    right: 10,
    pieces: [
      {
        lt: 6000,
        color: '#f5a623'
      },
      {
        gte: 6000,
        lte: 8000,
        color: '#26deca'
      },
      {
        gt: 8000,
        color: '#ed2939'
      },
    ],
    outOfRange: {
      color: '#999'
    }
  },

}));

async function mockData() {
  await new Promise(resolve => {
    setTimeout(resolve, 1000);
  });

  updateOptions(opts => {
    opts.xAxis.data = ['06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00', '24:00'];
    opts.series[0].data = [2208, 2016, 2916, 4512, 8281, 2008, 1963, 2367, 2956, 678];

    return opts;
  });
}

// function updateLocale() {
//   updateOptions((opts, factory) => {
//     const originOpts = factory();

//     opts.legend.data = originOpts.legend.data;
//     // opts.series[0].name = originOpts.series[0].name;
//     opts.series[0].name = "测量值";

//     return opts;
//   });
// }

async function init() {
  mockData();
}

// watch(
//   () => appStore.locale,
//   () => {
//     updateLocale();
//   }
// );

// init

onMounted(() => {
  mockData();

})

</script>

<template>
  <!-- <NCard :bordered="false" class="card-wrapper"> -->
  <div ref="domRef" class="h-300px overflow-hidden"></div>
  <!-- </NCard> -->
</template>

<style scoped></style>
