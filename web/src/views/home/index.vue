<!--
 * @Descripttion: 
 * @version: 0.x
 * @Author: zhai
 * @Date: 2024-06-25 17:09:30
 * @LastEditors: zhai
 * @LastEditTime: 2024-06-30 21:19:26
-->
<!--
 * @Descripttion: 
 * @version: 0.x
 * @Author: zhai
 * @Date: 2024-06-21 19:42:39
 * @LastEditors: zhai
 * @LastEditTime: 2024-06-30 21:14:42
-->

<template>
  <NSpace vertical :size="16">
    <n-card title="设备看板" :bordered="true" :segmented="{ content: true }">
      <n-spin :show="loading">
        <n-collapse v-if="expanded_names.length > 0" :default-expanded-names="expanded_names">
          <n-collapse-item v-for="(item, index) of equiptree" :key="item.group" :title="item.group" :name="item.group">
            <n-flex>
              <n-badge v-for="(equip, eindex) in item.equips" :show="equip.state != '0'" dot processing>
                <n-button :type="equip.state == '0' ? 'success' : 'warning'"
                  @click="routerPushByKey('early-warning_monitor', { query: { id: String(equip.equipID) } })"
                  style="border-radius: 0; width: 200px; height: 50px;">
                  <template #icon>
                    <icon-codicon:run-coverage v-if="equip.state == '0'" />
                    <icon-codicon:run-errors v-else />
                  </template>
                  <!-- <n-ellipsis style="max-width: 200px">
                  {{ equip.equipid }}
                </n-ellipsis> -->
                  {{ equip.equipID }}
                </n-button>
              </n-badge>
            </n-flex>
          </n-collapse-item>
        </n-collapse>
      </n-spin>
    </n-card>
  </NSpace>
</template>

<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue';

import { fast_equipment_api } from '@/service/api/ifd'
import { useRouterPush } from '@/hooks/common/router';
import { foxRequest } from '@/service/request';

const { routerPushByKey } = useRouterPush();

const loading = ref(true);

type Equipment = {
  TurID: string;
  equipID: string;
  state: string;
};

type GroupedEquipment = {
  group: string;
  equips: Equipment[];
};

const expanded_names = ref<string[]>([]);
const equiptree = ref<GroupedEquipment[]>([]);

const groupEquipments = (data: { equipmentList: Equipment[] }) => {
  const groupsMap: Record<string, GroupedEquipment> = {};

  data.equipmentList.forEach((equipment) => {
    const { TurID } = equipment;
    if (!groupsMap[TurID]) {
      groupsMap[TurID] = { group: TurID, equips: [] };
    }
    groupsMap[TurID].equips.push(equipment);
  });

  return {
    keys: Object.keys(groupsMap),
    tree: Object.values(groupsMap)
  }
};


async function refreshTree() {
  loading.value = true;

  //  mockRequest.get("/api/ft_alarm/mainStage");
  // let equipment_list = await fast_equipment_api.list(null, true);
  // const tree = generateTree(equipment_list.data.data);

  let ret = await foxRequest<any, 'json'>({
    url: "/api/ft_alarm/mainStage",
    method: 'post',
  });

  const { keys, tree } = groupEquipments(ret);

  expanded_names.value = keys;
  equiptree.value = tree;

  loading.value = false;
}

function handleClick(equipid) {

  // routerPushByKey('early-warning_monitor', { query: { a: '1' } })
  // routerPushByKey('early-warning_monitor', { params: { a: '1' } })

  // <NButton @click="routerPushByKey('early-warning_monitor', { query: { a: '1' } })">
}

onMounted(async () => {
  await refreshTree();

  // 随机状态
  // setInterval(function () {

  //   for (let item in equiptree.value) {
  //     if (item.children) {
  //       for (let node of item.children) {
  //         node.state = Math.random() > 0.5 ? 1 : 0;
  //       }
  //     }
  //   }
  // }, 3000);

  // nextTick(() => {
  //     if (treeContainer.value) {
  //         treeHeight.value = treeContainer.value.clientHeight - 20;
  //     }
  // });
});


</script>

<style scoped>
/* :deep(.n-button__content) {
  overflow-wrap: break-word;
} */

:deep(.n-button) {
  white-space: normal;
}
</style>
