<template>
    <div>

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
                            <!-- <template #cell_comment="scope">
                                <n-tag :type="scope.row.comment == '正常' ? 'success' : 'error'" @click="alert('')">
                                    {{ scope.row.comment }}
                                </n-tag>
                            </template> -->
                        </fs-crud>
                    </div>
                </n-card>
            </n-gi>
        </n-grid>
        <n-modal v-model:show="showModal" preset="card" title="历史数据" style="width: 80%; height: 90%">
            <n-flex justify="center" class="mb-8px">
                <n-input-group style="justify-content: center">
                    <n-button type="primary">
                        时间范围
                    </n-button>
                    <n-date-picker v-model:value="range" type="daterange" clearable />
                    <n-button type="primary" ghost>
                        搜索
                    </n-button>
                </n-input-group>
            </n-flex>

            <LineChart style="width: 100%; height:300px" />
            <n-divider />
            <PieChart style="width: 100%; height: 300px" />
        </n-modal>


        <n-modal v-model:show="showTip" preset="card" title="轴向位移2A偏高" style="width: 50%; height: 90%">
            <n-flex justify="center" class="mb-8px">
                <n-card title="可能的故障" size="small" :bordered="false">
                    <div class="tip-container">
                        <p>
                            <icon-ep:aim /> 主蒸汽参数、真空、机组负荷大幅度波动，造成轴向推力增加
                        </p>
                        <p>
                            <icon-ep:aim /> 汽轮机水冲击
                        </p>
                        <p>
                            <icon-ep:aim /> 推力瓦块乌金磨损，润滑油压过低或油温过高使油膜破坏
                        </p>
                        <p>
                            <icon-ep:aim /> 通流部分结垢、断叶片或漏汽严重，造成轴向推力增加
                        </p>
                        <p>
                            <icon-ep:aim /> 平衡鼓、汽封片磨损
                        </p>
                        <p>
                            <icon-ep:aim /> 抽汽运行方式发生变化
                        </p>
                        <p>
                            <icon-ep:aim /> 转子窜动
                        </p>
                    </div>
                </n-card>
                <n-card title="可能的维护措施" size="small" :bordered="false">
                    <div class="tip-container">
                        <p>
                            <icon-ep:aim /> 发现轴向位移增大时，应检查负荷、蒸汽参数、轴封汽温度、真空、润滑油温、推力瓦块温度、差胀等的变化，并设法调整，必要时通知热工校表
                        </p>
                        <p>
                            <icon-ep:aim /> 汽温、汽压降低时，通知锅炉提高进汽参数，并适当减少负荷使轴向位移降低
                        </p>
                        <p>
                            <icon-ep:aim /> 当轴向位移上升至报警值，汇报值长，采取降低负荷或适当调整抽汽运行方式使之下降至正常
                        </p>
                        <p>
                            <icon-ep:aim /> 当轴向位移上升并伴有不正常的响声，机组剧烈振动，应破坏真空紧急停机
                        </p>
                        <p>
                            <icon-ep:aim /> 汽轮机发生水冲击，应破坏真空紧急停机
                        </p>
                        <p>
                            <icon-ep:aim /> 如因叶片结垢严重使轴向位移增大时，汇报值长适当降低负荷，使轴向位移恢复至正常
                        </p>
                        <p>
                            <icon-ep:aim /> 轴向位移升至跳阐时，机组应自动跳闸，否则应紧急故障停机
                        </p>
                        <p>
                            <icon-ep:aim /> 轴向位移增大时，推力瓦块温度异常升高，任意一块瓦温升高至90°C时，减负荷;如升高至107°C时，应破坏真空紧急停机
                        </p>
                        <p>
                            <icon-ep:aim /> 机组升降负荷过程中，加强对振动等参数监视，保证蒸汽参数与负荷、缸温相匹配防止负荷 蒸汽参数大幅度变动保证汽水品质合格
                        </p>
                        <p>
                            <icon-ep:aim /> 加强对高/低加热器、除氧器运行监视，确保水位正常
                        </p>
                    </div>

                </n-card>
            </n-flex>
        </n-modal>

    </div>
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

const showModal = ref(false);
const showTip = ref(false);


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

import LineChart from './line-chart.vue';
import PieChart from './pie-chart.vue';

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
                    // type: 'text',
                    type: 'button',
                    column: {
                        component: {
                            type: compute(({ row, value }) => {
                                return row.comment == "正常" ? "success" : "error";
                            }),
                            size: 'small',
                            disabled: compute(({ row, value }) => {
                                return row.comment == "正常";
                            }),
                            on: {
                                onClick({ row }) {
                                    // message.success('按钮点击:' + row.warning);
                                    showTip.value = true;
                                },
                            },
                        },
                    },
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
                                    // message.success('按钮点击:' + row.warning);
                                    showModal.value = true;
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

.tip-container p {
    margin-bottom: 0.5em;
    /* 段落间距 */
}

.tip-container p:last-child {
    margin-bottom: 0;
    /* 移除最后一个段落的间距 */
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
