<template>

    <n-grid cols="1 s:1 m:1 l:5 xl:5 2xl:5" responsive="screen" :x-gap="12">
        <n-gi span="2">
            <n-card class="h-full" :segmented="{ content: true }" :bordered="false" size="small">
                <template #header>
                    <n-space>
                        <n-button type="info" ghost icon-placement="left" @click="addRoot">
                            启动
                            <template #icon>
                                <div>
                                    <icon-ic-outline-play-circle />
                                    <!-- <icon-mdi-emoticon class="text-24px text-red" /> -->
                                </div>
                            </template>
                        </n-button>
                    </n-space>
                </template>
                <div class="h-full w-full menu flex flex-col">
                    <n-input v-model:value="pattern" placeholder="输入设备名称搜索">
                        <template #suffix>
                            <n-icon size="18" class="cursor-pointer">
                                <SearchOutlined />
                            </n-icon>
                        </template>
                    </n-input>
                    <div ref="treeContainer" v-resize="onTreeContainerResize" style="height: 1px;"
                        class="py-3 flex-grow overflow-hidden">
                        <template v-if="loading">
                            <div class="flex items-center justify-center py-4">
                                <n-spin size="medium" />
                            </div>
                        </template>
                        <template v-else>
                            <n-tree :style="{ height: treeHeight + 'px' }" :virtual-scroll="true" block-line show-line
                                :draggable="false" :show-irrelevant-nodes="false" :pattern="pattern" :data="treeData"
                                key-field="id" label-field="name" :node-props="nodeProps">
                            </n-tree>
                        </template>
                    </div>
                </div>
            </n-card>
        </n-gi>
        <n-gi span="3">
            <n-card class="h-full" title="工况条件" :bordered="false">
                <template #header-extra>
                    数据每10秒更新一次
                </template>

                <div class="flex flex-col h-full">

                    <div class="flex flex-row justify-between">
                        <n-statistic v-for="item in statisticData" :key="item.id" v-bind="item"></n-statistic>
                    </div>

                    <fs-crud class="flex-grow" ref="crudRef" v-bind="crudBinding"> </fs-crud>
                </div>



            </n-card>
        </n-gi>
    </n-grid>


    <!-- 
                    <n-space :size="12" :wrap="false">
                    </n-space> -->

    <!-- <div flex items-center>
                        <img rounded-full width="60" :src="userStore.avatar" />
                        <div ml-10>
                            <p text-20 font-semibold>
                                {{ $t('views.workbench.text_hello', { username: userStore.name }) }}
                            </p>
                            <p mt-5 text-14 op-60>{{ $t('views.workbench.text_welcome') }}</p>
                        </div>
                    </div> -->
    <!-- 
                    <n-alert v-if="curEquipment == null" type="info" closable>
                        从设备列表选择一项后，进行关联
                    </n-alert>
                    <n-flex v-else class="h-full">
                        <mfst class="flex-grow" :selkeys="keysmfst" @select-types="onSelectMfst"> </mfst>
                        <mfpt class="flex-grow" :selkeys="keysmfpt" @select-types="onSelectMfpt"> </mfpt>
                    </n-flex> -->
</template>
<script lang="ts" setup>


import { ref, unref, reactive, onMounted, computed, Ref, nextTick } from 'vue';
import { TreeOption, useDialog, useMessage } from 'naive-ui';
import { AddReq, CreateCrudOptionsProps, CreateCrudOptionsRet, DelReq, EditReq, UserPageQuery, UserPageRes, compute, useColumns, useFormWrapper, useFs } from '@fast-crud/fast-crud';
import { equipment_api, fast_equipment_api } from './api'
import { fast_mfst_api as api } from '@/views/ifd/mfs/api';

import { $t } from '@/locales';

const { openDialog } = useFormWrapper();

const message = useMessage();
const dialog = useDialog();


const treeData = ref([]);

const loading = ref(true);
const treeItemTitle = ref('');
const pattern = ref('');

const treeHeight: Ref<number> = ref(0);
const treeContainer: Ref<HTMLDivElement | null> = ref(null);

const curEquipment = ref(null);

const nodeProps = ({ option }: { option: TreeOption }) => {
    return {
        onClick() {
            curEquipment.value = option;
        },
    }
}

const statisticData = ref([
    {
        id: 0,
        label: $t('当前时间戳'),
        value: '2024-6-16 10:33:22',
    },
    {
        id: 1,
        label: $t('有功功率'),
        value: '17MV',
    },
    {
        id: 2,
        label: $t('环境温度'),
        value: '5℃',
    },
    {
        id: 3,
        label: $t('汽机转速'),
        value: '3000rpm',
    },
]);


const formParams = reactive({
    type: 1,
    label: '',
    subtitle: '',
    path: '',
    auth: '',
    openType: 1,
});



function generateTree(items) {
    const map = {};
    const tree = [];

    items.forEach(item => {
        map[item.id] = item;
    });

    items.forEach(item => {
        if (item.parent_id !== null && item.parent_id !== 0) {
            if (!("children" in map[item.parent_id])) {
                map[item.parent_id].children = [];
            }
            map[item.parent_id].children.push(map[item.id]);
        } else {
            tree.push(map[item.id]);
        }
    });

    return tree;
}


/**
*  找到对应的节点
* */
let result = null;
function getTreeItem(data: any[], key?: string | number): any {
    data.map((item) => {
        if (item.key === key) {
            result = item;
        } else {
            if (item.children && item.children.length) {
                getTreeItem(item.children, key);
            }
        }
    });
    return result;
}


async function addRoot() {

}



function createCrudOptions({ crudExpose }: CreateCrudOptionsProps): CreateCrudOptionsRet {
    const pageRequest = async (query: UserPageQuery): Promise<UserPageRes> => {
        return api.GetList(query);
    };
    const editRequest = async (ctx: EditReq) => {
        const { form, row } = ctx;
        form.id = row.id;
        return api.UpdateObj(form);
    };
    const delRequest = async (ctx: DelReq) => {
        const { row } = ctx;
        return api.DelObj(row.id);
    };

    const addRequest = async (req: AddReq) => {
        const { form } = req;
        return api.AddObj(form);
    };

    return {
        crudOptions: {
            container: {
                // is: 'fs-layout-card'
            },
            request: {
                pageRequest,
                addRequest,
                editRequest,
                delRequest
            },
            settings: {
                plugins: {}
            },
            table: {
                striped: true
            },
            toolbar: {
                show: false,
            },
            actionbar: {
                show: false,
            },
            rowHandle: {
                show: false,
            },
            search: {
                show: false
            },
            pagination: {
                show: false
            },
            form: {
                wrapper: {
                    draggable: false,
                }
            },
            columns: {
                id: {
                    title: 'ID',
                    key: 'id',
                    type: 'number',
                    column: {
                        show: false,
                        width: 50
                    },
                    form: {
                        show: false
                    }
                },


                parameter: {
                    title: '参数',
                    type: 'text',
                },
                unit: {
                    title: '单位',
                    type: 'text',
                },
                value: {
                    title: '实时值',
                    type: 'text',
                },
                lowerbound: {
                    title: '下限',
                    type: 'text',
                },
                upperbound: {
                    title: '上限',
                    type: 'text',
                },
                comment: {
                    title: '评语',
                    type: 'text',
                },
                warning: {
                    title: '故障预警',
                    type: 'button',
                    column: {
                        component: {
                            type: 'success',
                            size: 'small',
                            show: compute(({ value }) => {
                                //当value为null时，不显示
                                return value != null;
                            }),
                            on: {
                                onClick({ row }) {
                                    message.success('按钮点击:' + row.warning);
                                },
                            },
                        },
                    },
                },
            }
        }
    };
}

const { crudRef, crudBinding, crudExpose } = useFs({ createCrudOptions });

// 页面打开后获取列表数据
onMounted(() => {
    crudExpose.doRefresh();
});

// function createData(level = 4, baseKey = ''): TreeOption[] | undefined {
//     if (!level) return undefined
//     return repeat(6 - level, undefined).map((_, index) => {
//         const key = '' + baseKey + level + index
//         const label = createLabel(level)
//         return {
//             label,
//             key,
//             children: createData(level - 1, key),
//             suffix: () =>
//                 h(
//                     NButton,
//                     { text: true, type: 'primary' },
//                     { default: () => 'Suffix' }
//                 ),
//             prefix: () =>
//                 h(NButton, { text: true, type: 'primary' }, { default: () => 'Prefix' })
//         }
//     })
// }

async function refreshTree() {
    loading.value = true;
    let equipment_list = await equipment_api.list(null, true);

    const treeMenuList = generateTree(equipment_list.data.data);
    treeData.value = treeMenuList;
    loading.value = false;
}

function onTreeContainerResize({ width, height }) {
    treeHeight.value = height - 20;
}

onMounted(async () => {
    await refreshTree();

    nextTick(() => {
        if (treeContainer.value) {
            treeHeight.value = treeContainer.value.clientHeight - 20;
        }
    });

    // const keys = treeMenuList.map((item) => item.id);
    // Object.assign(formParams, keys);

    // treeData.value = treeMenuList;
    // loading.value = false;
});


</script>


<style scoped>
:deep(.fs-crud-footer) {
    display: none;
}

.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 0px;
}
</style>
