<template>
    <n-flex vertical class="h-full">

        <n-grid class="flex-grow" cols="1 s:1 m:1 l:2 xl:2 2xl:2" responsive="screen" :x-gap="12">
            <n-gi span="1">
                <n-card title="故障征兆类型" class="h-full" size="small" :segmented="{ content: true }">
                    <mfst @select-type="onSelectType"> </mfst>
                </n-card>
            </n-gi>
            <n-gi span="1">
                <n-card title="故障征兆" class="h-full" size="small" :segmented="{ content: true }">
                    <mfs :type_id="selectedType"> </mfs>
                </n-card>
            </n-gi>
        </n-grid>
    </n-flex>
</template>

<script lang="ts" setup>
import { ref, unref, reactive, onMounted, computed, Ref, nextTick } from 'vue';
import { useDialog, useMessage } from 'naive-ui';

import { useColumns, useFormWrapper } from '@fast-crud/fast-crud';
import mfst from './mfst.vue';
import mfs from './mfs.vue';
import { fast_equipment_api } from '@/service/api/ifd';


const { openDialog } = useFormWrapper();


const formRef: any = ref(null);
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

const selectedType = ref<number | null>(null);

function onSelectType(value: number | null) {
    selectedType.value = value;
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

    let ret = await fast_equipment_api.DelObj(option.id);
    if (!ret.error) {
        message.success('删除成功');
        await refreshTree();
    }
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




function selectedTree(keys) {
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
    let equipment_list = await fast_equipment_api.list();
    const treeMenuList = generateTree(equipment_list.data.data);
    treeData.value = treeMenuList;
    loading.value = false;
}

function onTreeContainerResize({ width, height }) {
    treeHeight.value = height - 22;
}

onMounted(async () => {
    // await refreshTree();

    // nextTick(() => {
    //     if (treeContainer.value) {
    //         treeHeight.value = treeContainer.value.clientHeight - 22;
    //     }
    // });

    // const keys = treeMenuList.map((item) => item.id);
    // Object.assign(formParams, keys);

    // treeData.value = treeMenuList;
    // loading.value = false;
});


</script>


<style scoped>
.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 0px;
}
</style>
