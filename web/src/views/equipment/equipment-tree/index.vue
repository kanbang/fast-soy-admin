<template>
    <n-flex vertical class="h-full">
        <div class="n-layout-page-header w-full">
            <n-card :bordered="false" title="设备树管理">
                <!-- 示例数据。 -->
            </n-card>
        </div>
        <n-grid class="flex-grow" cols="1 s:1 m:1 l:5 xl:5 2xl:5" responsive="screen" :x-gap="12">
            <n-gi span="2">
                <n-card class="h-full" :segmented="{ content: true }" :bordered="false" size="small">
                    <template #header>
                        <n-button type="info" ghost icon-placement="left" @click="addRoot" size="small">
                            添加根节点
                            <template #icon>
                                <div>
                                    <icon-pajamas-file-tree />
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
                                <x-n-tree :style="{ height: treeHeight + 'px' }" :virtual-scroll="true" block-line
                                    show-line :draggable="false" :show-irrelevant-nodes="false" :pattern="pattern"
                                    :data="treeData" key-field="id" label-field="name" :node-props="nodeProps">

                                    <!-- style="max-height: 350px; overflow: hidden" -->
                                    <template #render-label="{ option }">
                                        <span class="custom-tree-node">
                                            <span>{{ option.name }}</span>
                                            <span>
                                                <n-button @click="addChildNode(option)" ghost size="small"
                                                    type="primary">
                                                    添加子节点
                                                </n-button>
                                                <n-button @click="editNode(option)" ghost size="small" type="info"
                                                    style="margin-left: 8px">
                                                    编辑
                                                </n-button>
                                                <n-button @click="delNode(option)" ghost size="small" type="error"
                                                    style="margin-left: 8px">
                                                    删除
                                                </n-button>
                                            </span>
                                        </span>

                                    </template>
                                </x-n-tree>
                            </template>
                        </div>
                    </div>
                </n-card>
            </n-gi>
            <n-gi span="3">
                <n-card class="h-full" :segmented="{ content: true }" :bordered="false" size="small">
                    <template #header>
                        关联征兆现象{{ treeItemTitle ? `：${treeItemTitle} ` : '' }}
                    </template>

                    <n-alert v-if="curEquipment == null" type="info" closable>
                        从设备列表选择一项后，进行关联
                    </n-alert>
                    <n-flex v-else class="h-full">
                        <mfst class="flex-grow" :selkeys="keysmfst" @select-types="onSelectMfst"> </mfst>
                        <mfpt class="flex-grow" :selkeys="keysmfpt" @select-types="onSelectMfpt"> </mfpt>
                    </n-flex>
                </n-card>
            </n-gi>
        </n-grid>

        <CreateDrawer ref="createDrawerRef" :title="drawerTitle" />
    </n-flex>
</template>
<script lang="ts" setup>


import { ref, unref, reactive, onMounted, computed, Ref, nextTick } from 'vue';
import { TreeOption, useDialog, useMessage } from 'naive-ui';
// import { DownOutlined, AlignLeftOutlined, SearchOutlined, FormOutlined } from '@vicons/antd';
// import { getMenuList } from '@/api/system/menu';
// import { getTreeItem } from '@/utils';
import CreateDrawer from './CreateDrawer.vue';
import { XNTree } from '@skit/x.naive-ui';
import { useColumns, useFormWrapper } from '@fast-crud/fast-crud';
import mfst from './mfst.vue';
import mfpt from './mfpt.vue';
import { fast_equipment_api } from '@/service/api/ifd'

const { openDialog } = useFormWrapper();

const rules = {
    label: {
        required: true,
        message: '请输入标题',
        trigger: 'blur',
    },
    path: {
        required: true,
        message: '请输入路径',
        trigger: 'blur',
    },
};

const formRef: any = ref(null);
const createDrawerRef = ref();
const message = useMessage();
const dialog = useDialog();

let treeItemKey = ref([]);

let expandedKeys = ref([]);

const treeData = ref([]);

const loading = ref(true);
const subLoading = ref(false);
const isEditMenu = ref(false);
const treeItemTitle = ref('');
const pattern = ref('');
const drawerTitle = ref('');

const treeHeight: Ref<number> = ref(0);
const treeContainer: Ref<HTMLDivElement | null> = ref(null);

const curEquipment = ref(null);

const keysmfst = computed(() => {
    if (curEquipment.value == null || curEquipment.value.mfsts_refids == null) {
        return [];
    }

    return curEquipment.value.mfsts_refids;
});

const keysmfpt = computed(() => {
    if (curEquipment.value == null || curEquipment.value.mfpts_refids == null) {
        return [];
    }

    return curEquipment.value.mfpts_refids;
});


const nodeProps = ({ option }: { option: TreeOption }) => {
    return {
        onClick() {
            // message.info('[Click] ' + JSON.stringify(option))
            curEquipment.value = option;
            treeItemTitle.value = option.name;

        },
        // onContextmenu(e: MouseEvent): void {
        //     optionsRef.value = [option]
        //     showDropdownRef.value = true
        //     xRef.value = e.clientX
        //     yRef.value = e.clientY
        //     console.log(e.clientX, e.clientY)
        //     e.preventDefault()
        // }
    }
}


function onSelectMfst(value: Array<number>) {
    console.log(value);
    if (curEquipment.value) {
        curEquipment.value.mfsts_refids = value;
        fast_equipment_api.update(curEquipment.value);
    }    // keysmfst.value = value;
}

function onSelectMfpt(value: Array<number>) {
    console.log(value);
    if (curEquipment.value) {
        curEquipment.value.mfpts_refids = value;
        fast_equipment_api.update(curEquipment.value);
    }    // keysmfst.value = value;
}


function createTreeFormOptions(message: any) {
    const { buildFormOptions } = useColumns();
    return buildFormOptions({
        columns: {
            name: {
                title: '名称',
                form: {
                    component: {
                        name: 'n-input',
                        vModel: 'value',
                        allowClear: true,
                    },
                    rules: [{ required: true, message: '此项必填' }],
                },
            },
            type: {
                title: '类型',
                form: {
                    component: {
                        name: 'n-input',
                        vModel: 'value',
                        allowClear: true,
                    },
                    rules: [{ required: true, message: '此项必填' }],
                },
            },
        },
        form: {
            wrapper: {
                title: '设备',
                draggable: false,
            },
            labelCol: { span: 6 },
            async doSubmit({ form }) {
                if ("id" in form) {
                    let ret = await fast_equipment_api.UpdateObj(form);
                    if (!ret.error) {
                        message.success('更新成功');
                        await refreshTree();
                    }
                }
                else {
                    let ret = await fast_equipment_api.AddObj(form);
                    if (!ret.error) {
                        message.success('添加成功');
                        await refreshTree();
                    }
                }
            },
        },
    });
}


const formParams = reactive({
    type: 1,
    label: '',
    subtitle: '',
    path: '',
    auth: '',
    openType: 1,
});



// function generateTree(items) {
//     const map = {};
//     const tree = [];

//     items.forEach(item => {
//         map[item.id] = { ...item, children: [] };
//     });

//     items.forEach(item => {
//         if (item.parent_id !== null && item.parent_id !== 0) {
//             map[item.parent_id].children.push(map[item.id]);
//         } else {
//             tree.push(map[item.id]);
//         }
//     });

//     return tree;
// }

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


async function addChildNode(option: any) {
    // console.log(option)
    const opts = createTreeFormOptions(message);
    opts.initialForm = { parent_id: option.id, name: '初始值' };
    const wrapperRef = await openDialog(opts);
}

async function editNode(option: any) {
    // console.log(option)
    const opts = createTreeFormOptions(message);
    opts.initialForm = option;
    const wrapperRef = await openDialog(opts);
}

async function delNode(option: any) {
    // console.log(option)

    dialog.info({
        title: '提示',
        content: `您确定想删除此节点吗?`,
        positiveText: '确定',
        negativeText: '取消',
        onPositiveClick: async () => {
            let ret = await fast_equipment_api.DelObj(option.id);
            if (!ret.error) {
                message.success('删除成功');
                await refreshTree();
            }
        },
        onNegativeClick: () => {
            message.error('已取消');
        },
    });
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



function openCreateDrawer() {
    const { openDrawer } = createDrawerRef.value;
    openDrawer();
}

function selectedTree(keys) {
    debugger
    if (keys.length) {
        const treeItem = getTreeItem(unref(treeData), keys[0]);
        treeItemKey.value = keys;
        treeItemTitle.value = treeItem.label;
        Object.assign(formParams, treeItem);
        isEditMenu.value = true;
    } else {
        isEditMenu.value = false;
        treeItemKey.value = [];
        treeItemTitle.value = '';
    }
}

function handleDel() {
    dialog.info({
        title: '提示',
        content: `您确定想删除此权限吗?`,
        positiveText: '确定',
        negativeText: '取消',
        onPositiveClick: () => {
            message.success('删除成功');
        },
        onNegativeClick: () => {
            message.error('已取消');
        },
    });
}

function handleReset() {
    const treeItem = getTreeItem(unref(treeData), treeItemKey.value[0]);
    Object.assign(formParams, treeItem);
}

function formSubmit() {
    formRef.value.validate((errors: boolean) => {
        if (!errors) {
            message.error('抱歉，您没有该权限');
        } else {
            message.error('请填写完整信息');
        }
    });
}

async function addRoot() {
    // 侧栏操作
    // openCreateDrawer();

    const opts = createTreeFormOptions(message);
    opts.initialForm = { name: '初始值' };

    const wrapperRef = await openDialog(opts);
    console.log('对话框已打开', wrapperRef);
}


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
    let equipment_list = await fast_equipment_api.list(null, true);

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
:deep(.n-card-header) {
    height: 48px;
}

:deep(.fs-crud-header) {
    display: none;
}

:deep(.fs-container) {
    background-color: none;
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
