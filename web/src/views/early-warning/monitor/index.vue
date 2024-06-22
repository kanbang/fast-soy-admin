<template>

    <n-grid cols="1 s:1 m:1 l:5 xl:5 2xl:5" responsive="screen" :x-gap="12">
        <n-gi span="2">
            <n-card class="h-full" :segmented="{ content: true }" :bordered="false" size="small">
                <template #header>
                    <n-button type="info" ghost icon-placement="left" size="small" @click="onStart">
                        启动
                        <template #icon>
                            <div>
                                <icon-ic-outline-play-circle />
                                <!-- <icon-mdi-emoticon class="text-24px text-red" /> -->
                            </div>
                        </template>
                    </n-button>
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
                            <n-tree :style="{ height: treeHeight + 'px' }" :virtual-scroll="true" default-expand-all
                                :default-selected-keys="selectedItem" block-line show-line :draggable="false"
                                :show-irrelevant-nodes="false" :pattern="pattern" :data="treeData" key-field="id"
                                label-field="name" :node-props="treeNodeProps">
                            </n-tree>
                        </template>
                    </div>
                </div>
            </n-card>
        </n-gi>
        <n-gi span="3">
            <n-card class="h-full" title="工况条件" :bordered="false" :segmented="{ content: true }" size="small">
                <template #header-extra>
                    数据每10秒更新一次
                </template>

                <div class="flex flex-col h-full">
                    <div class="flex flex-row justify-between">
                        <n-statistic v-for="item in statisticData" :key="item.id" v-bind="item"></n-statistic>
                    </div>
                    <n-divider />
                    <fs-crud class="flex-grow" ref="crudRef" v-bind="crudBinding">
                        <template #cell_comment="scope">
                            <n-tag :type="scope.row.comment == '正常' ? 'success' : 'error'">
                                {{ scope.row.comment }}
                            </n-tag>
                        </template>
                    </fs-crud>
                </div>
            </n-card>
        </n-gi>
    </n-grid>
</template>
<script lang="ts" setup>


import { ref, unref, reactive, onMounted, computed, Ref, nextTick } from 'vue';
import { TreeOption, useDialog, useMessage } from 'naive-ui';
import { AddReq, CreateCrudOptionsProps, CreateCrudOptionsRet, DelReq, EditReq, UserPageQuery, UserPageRes, compute, useColumns, useFormWrapper, useFs } from '@fast-crud/fast-crud';
import { fast_mfst_api, fast_equipment_api } from '@/service/api/ifd';

import { $t } from '@/locales';
import { useRoute } from 'vue-router';

const { openDialog } = useFormWrapper();

const message = useMessage();
const dialog = useDialog();



interface ITreeItem {
    id: number;
    parent_id: number | null;
    children?: ITreeItem[];
}


const treeData = ref<ITreeItem[]>([]);

const loading = ref(true);
const pattern = ref('');

const selectedItem = ref([]);


const curEquipment = ref<TreeOption | null>(null);


const treeHeight: Ref<number> = ref(0);
const treeContainer: Ref<HTMLDivElement | null> = ref(null);


const treeNodeProps = ({ option }: { option: TreeOption }) => {
    return {
        onClick() {
            curEquipment.value = option;
            crudExpose.doRefresh();
        },
    }
}

const route = useRoute();

const routeQuery = computed(() => JSON.stringify(route.query));


const statisticData = ref([
    {
        id: 0,
        label: $t('当前时间戳'),
        value: '2024-6-16 10:33:22',
    },
    {
        id: 1,
        label: ('有功功率'),
        value: '17MV',
    },
    {
        id: 2,
        label: ('环境温度'),
        value: '5℃',
    },
    {
        id: 3,
        label: ('汽机转速'),
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


let treeItemMap: { [key: number]: ITreeItem } = {};

function generateTree(items: ITreeItem[]): ITreeItem[] {
    treeItemMap = {};
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
    let equipment_list = await fast_equipment_api.list(null, true);

    const tree = generateTree(equipment_list.data.data);
    treeData.value = tree;
    loading.value = false;


}

function onTreeContainerResize({ width, height }) {
    treeHeight.value = height - 20;
}

async function onStart() {

}


function createCrudOptions({ crudExpose }: CreateCrudOptionsProps): CreateCrudOptionsRet {
    const pageRequest = async (query: UserPageQuery): Promise<UserPageRes> => {

        let demodata = [
            {
                "index": 1,
                "parameter": "1号轴承1号金属温度（炉侧）",
                "unit": "°C",
                "value": 54.84,
                "lower_limit": 55,
                "upper_limit": 55,
                "comment": "偏低",
                "warning": "查询"
            },
            {
                "index": 2,
                "parameter": "1号轴承2号金属温度（靠侧）",
                "unit": "°C",
                "value": null,
                "lower_limit": 0,
                "upper_limit": 99,
                "comment": "正常",
                "warning": "查询"
            },
            {
                "index": 3,
                "parameter": "1号轴径振动（X方向）",
                "unit": "μm",
                "value": 47.95,
                "lower_limit": 0,
                "upper_limit": 120,
                "comment": "正常",
                "warning": "查询"
            },
            {
                "index": 4,
                "parameter": "1号轴径振动（Y方向）",
                "unit": "μm",
                "value": 47.95,
                "lower_limit": 0,
                "upper_limit": 48,
                "comment": "偏低",
                "warning": "查询"
            },
            {
                "index": 5,
                "parameter": "2号轴承1号金属温度（炉侧）",
                "unit": "°C",
                "value": 89.7,
                "lower_limit": 0,
                "upper_limit": 99,
                "comment": "正常",
                "warning": "查询"
            },
            {
                "index": 6,
                "parameter": "2号轴承2号金属温度（靠侧）",
                "unit": "°C",
                "value": 47.95,
                "lower_limit": 0,
                "upper_limit": 99,
                "comment": "正常",
                "warning": "查询"
            }
        ];

        return {
            code: 0, data: {
                data: demodata,
                meta: {
                    total: 6
                }
            }
        };
    };

    const editRequest = async (ctx: EditReq) => { };
    const delRequest = async (ctx: DelReq) => { };
    const addRequest = async (req: AddReq) => { };

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
                    },
                    form: {
                        show: false
                    }
                },

                parameter: {
                    title: '参数',
                    type: 'text',
                    column: {
                        width: 260,
                    },
                },
                unit: {
                    title: '单位',
                    type: 'text',
                },
                value: {
                    title: '实时值',
                    type: 'text',
                },
                lower_limit: {
                    title: '下限',
                    type: 'text',
                },
                upper_limit: {
                    title: '上限',
                    type: 'text',
                },

                // <n-tag type="success">
                //   不该
                // </n-tag>
                // <n-tag type="warning">
                //   超人不会飞
                // </n-tag>
                // <n-tag type="error">
                //   手写的从前
                // </n-tag>
                comment: {
                    title: '评语',
                    type: 'text',
                },
                warning: {
                    title: '故障预警',
                    type: 'button',
                    column: {
                        component: {
                            type: compute(({ row, value }) => {
                                return row.comment == "正常" ? "tertiary" : "success";
                            }),
                            size: 'small',
                            disabled: compute(({ row, value }) => {
                                return row.comment == "正常";
                            }),

                            // show: compute(({ value }) => {
                            //     return value != null;
                            // }),
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


onMounted(async () => {
    // message.info(route.params   );
    // message.info(JSON.stringify(route.query));

    let selected_id = null;
    if ("id" in route.query) {
        selected_id = +route.query.id;
        selectedItem.value = [selected_id];
    }

    await refreshTree();

    nextTick(() => {
        if (treeContainer.value) {
            treeHeight.value = treeContainer.value.clientHeight - 20;
        }

        if (selected_id != null && selected_id in treeItemMap) {
            curEquipment.value = treeItemMap[selected_id];
            crudExpose.doRefresh();
        }
    });
});


</script>


<style scoped>
:deep(.n-card-header) {
    height: 48px;
}

:deep(.fs-crud-footer) {
    display: none;
}

:deep(.fs-crud-header) {
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
