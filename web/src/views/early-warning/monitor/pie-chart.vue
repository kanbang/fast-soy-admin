<script setup lang="ts">
import { onMounted, watch } from 'vue';
import { $t } from '@/locales';
import { useAppStore } from '@/store/modules/app';
import { useEcharts } from '@/hooks/common/echarts';

defineOptions({
  name: 'PieChart'
});

interface SeriesItem {
  name: string;
  data: number;
}

interface Props {
  piedata: SeriesItem[]
}

const props = withDefaults(defineProps<Props>(), {
  piedata: [],
});


const appStore = useAppStore();

const { domRef, updateOptions } = useEcharts(() => ({
  title: {
    text: '指标评价历史饼图'
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    bottom: '1%',
    left: 'center',
    itemStyle: {
      borderWidth: 0
    }
  },
  series: [
    {
      color: [ '#26deca', '#f5a623', '#ed2939'],
      name: $t('page.home.schedule'),
      type: 'pie',
      radius: ['45%', '75%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 1
      },
      label: {
        show: true,
        // formatter: '{b}: {@2012} ({d}%)'
        formatter: '{b}: {@v} ({d}%)'
        // position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: '12'
        }
      },
      labelLine: {
        show: true
      },
      data: [] as { name: string; value: number }[]
    }
  ]
}));

async function mockData() {
  await new Promise(resolve => {
    setTimeout(resolve, 1000);
  });

  updateOptions(opts => {
    // opts.series[0].data = [
    //   { name: "正常", value: 40 },
    //   { name: "偏低", value: 10 },
    //   { name: "偏高", value: 20 },
    // ];

    opts.series[0].data = props.piedata;

    return opts;
  });
}

function updateLocale() {
  updateOptions((opts, factory) => {
    const originOpts = factory();

    opts.series[0].name = originOpts.series[0].name;

    opts.series[0].data = [
      { name: $t('page.home.study'), value: 20 },
      { name: $t('page.home.entertainment'), value: 10 },
      { name: $t('page.home.work'), value: 40 },
      { name: $t('page.home.rest'), value: 30 }
    ];

    return opts;
  });
}

async function init() {
  mockData();
}

watch(
  () => appStore.locale,
  () => {
    updateLocale();
  }
);
onMounted(() => {
  mockData();

})

// init
init();
</script>

<template>
  <!-- <NCard :bordered="false" class="card-wrapper"> -->
    <div ref="domRef" class="h-300px overflow-hidden"></div>
  <!-- </NCard> -->
</template>

<style scoped></style>
