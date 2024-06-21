<script setup lang="ts">
import { computed, ref } from 'vue';
import { useAppStore } from '@/store/modules/app';
// import HeaderBanner from './modules/header-banner.vue';
// import CardData from './modules/card-data.vue';
// import LineChart from './modules/line-chart.vue';
// import PieChart from './modules/pie-chart.vue';
// import ProjectNews from './modules/project-news.vue';
// import CreativityBanner from './modules/creativity-banner.vue';

const appStore = useAppStore();

const gap = computed(() => (appStore.isMobile ? 0 : 16));

const equiptree = ref([
  {
    group: "机组1",
    equips: [
      {
        equipid: "风机1风机1风机1风机1风机1风机1风机1风机1风机1",
        state: 0
      },
      {
        equipid: "风机1",
        state: 0
      },
      {
        equipid: "风机1",
        state: 1
      },
      {
        equipid: "风机1",
        state: 0
      },
      {
        equipid: "风机1",
        state: 0
      },
      {
        equipid: "风机1",
        state: 1
      },
      {
        equipid: "风机1",
        state: 0
      },
      {
        equipid: "风机1",
        state: 0
      }
    ]
  },

  {
    group: "机组2",
    equips: [
      {
        equipid: "风机1",
        state: 0
      },
      {
        equipid: "风机1",
        state: 0
      },
      {
        equipid: "风机1",
        state: 1
      },
      {
        equipid: "风机1",
        state: 0
      },
      {
        equipid: "风机1",
        state: 0
      },
      {
        equipid: "风机1",
        state: 1
      },
      {
        equipid: "风机1",
        state: 0
      },
      {
        equipid: "风机1",
        state: 0
      }
    ]
  }
])
</script>

<template>
  <NSpace vertical :size="16">
    <n-card title="设备看板" :bordered="true" :segmented="{ content: true }">
      <n-collapse :default-expanded-names="[0, 1]">
        <n-collapse-item v-for="(node, index) in equiptree" :key="index" :title="node.group" :name="index">
          <n-flex>
            <n-badge v-for="(equip, eindex) in node.equips" :show="equip.state" dot processing>
              <n-button :type="equip.state == 0 ? 'success' : 'warning'"
                style="border-radius: 0; width: 200px; height: 50px;">
                <template #icon>
                  <icon-codicon:run-coverage v-if="equip.state == 0" />
                  <icon-codicon:run-errors v-else />
                </template>
                <!-- <n-ellipsis style="max-width: 200px">
                  {{ equip.equipid }}
                </n-ellipsis> -->
                {{ equip.equipid }}
              </n-button>
            </n-badge>
          </n-flex>
        </n-collapse-item>
      </n-collapse>
    </n-card>
  </NSpace>

  <!-- 
  <NSpace vertical :size="16">


    <HeaderBanner />
    <CardData />
    <NGrid :x-gap="gap" :y-gap="16" responsive="screen" item-responsive>
      <NGi span="24 s:24 m:14">
        <NCard :bordered="false" class="card-wrapper">
          <LineChart />
        </NCard>
      </NGi>
      <NGi span="24 s:24 m:10">
        <NCard :bordered="false" class="card-wrapper">
          <PieChart />
        </NCard>
      </NGi>
    </NGrid>
    <NGrid :x-gap="gap" :y-gap="16" responsive="screen" item-responsive>
      <NGi span="24 s:24 m:14">
        <ProjectNews />
      </NGi>
      <NGi span="24 s:24 m:10">
        <CreativityBanner />
      </NGi>
    </NGrid>
  </NSpace> -->
</template>

<style scoped>
/* :deep(.n-button__content) {
  overflow-wrap: break-word;
} */

:deep(.n-button) {
  white-space: normal;
}
</style>
