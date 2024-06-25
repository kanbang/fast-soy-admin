<!--
 * @Descripttion: 
 * @version: 0.x
 * @Author: zhai
 * @Date: 2024-06-21 19:42:39
 * @LastEditors: zhai
 * @LastEditTime: 2024-06-22 22:18:57
-->

<template>
  <NSpace vertical :size="16">
    <n-card title="设备看板" :bordered="true" :segmented="{ content: true }">
      <n-spin :show="loading">
        <n-collapse v-if="expanded_names.length > 0" :default-expanded-names="expanded_names">
          <n-collapse-item v-for="(value, key, index) in equiptree" :key="index" :title="key" :name="key">
            <n-flex>
              <n-badge v-for="(equip, eindex) in value" :show="equip.state != '0'" dot processing>
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

// const equiptree = ref([
//   {
//     group: "机组1",
//     equips: [
//       {
//         equipid: "风机1风机1风机1风机1风机1风机1风机1风机1风机1",
//         state: 0
//       },
//       {
//         equipid: "风机1",
//         state: 0
//       },
//       {
//         equipid: "风机1",
//         state: 1
//       },
//       {
//         equipid: "风机1",
//         state: 0
//       },
//       {
//         equipid: "风机1",
//         state: 0
//       },
//       {
//         equipid: "风机1",
//         state: 1
//       },
//       {
//         equipid: "风机1",
//         state: 0
//       },
//       {
//         equipid: "风机1",
//         state: 0
//       }
//     ]
//   },

//   {
//     group: "机组2",
//     equips: [
//       {
//         equipid: "风机1",
//         state: 0
//       },
//       {
//         equipid: "风机1",
//         state: 0
//       },
//       {
//         equipid: "风机1",
//         state: 1
//       },
//       {
//         equipid: "风机1",
//         state: 0
//       },
//       {
//         equipid: "风机1",
//         state: 0
//       },
//       {
//         equipid: "风机1",
//         state: 1
//       },
//       {
//         equipid: "风机1",
//         state: 0
//       },
//       {
//         equipid: "风机1",
//         state: 0
//       }
//     ]
//   }
// ])

const loading = ref(true);


interface ITreeItem {
  id: number;
  parent_id: number | null;
  children?: ITreeItem[];
}

const expanded_names = ref<number[]>([]);
const equiptree = ref<ITreeItem[]>([]);

function generateTree(items: ITreeItem[]): ITreeItem[] {
  const treeItemMap: { [key: number]: ITreeItem } = {};
  const tree: ITreeItem[] = [];

  // 建立 ID 到 item 的映射
  items.forEach(item => {
    treeItemMap[item.id] = item;
  });

  // 构建树结构
  items.forEach(item => {
    if (item.parent_id !== null && item.parent_id !== 0) {
      const parent = treeItemMap[item.parent_id];
      if (parent) {
        if (!parent.children) {
          parent.children = [];
        }
        parent.children.push(treeItemMap[item.id]);
      }
    } else {
      tree.push(treeItemMap[item.id]);
    }
  });

  return tree;
}


async function refreshTree() {
  loading.value = true;

  //  mockRequest.get("/api/ft_alarm/mainStage");



  // let equipment_list = await fast_equipment_api.list(null, true);

  // const tree = generateTree(equipment_list.data.data);
  
  let tree = await foxRequest<any, 'json'>({
    url: "/api/ft_alarm/mainStage",
    method: 'post',
  });


  expanded_names.value = Object.keys(tree);
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
