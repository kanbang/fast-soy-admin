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
                        <n-space>
                            <n-button type="info" ghost icon-placement="left" @click="addRoot">
                                添加根节点
                                <template #icon>
                                    <div>
                                        <icon-pajamas-file-tree />
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
                        <div ref="treeContainer" v-resize="onTreeContainerResize" class="py-3 menu-list flex-grow">
                            <template v-if="loading">
                                <div class="flex items-center justify-center py-4">
                                    <n-spin size="medium" />
                                </div>
                            </template>
                            <template v-else>
                                <x-n-tree :style="{ height: treeHeight + 'px' }" :virtual-scroll="true" block-line
                                    show-line :draggable="false" :show-irrelevant-nodes="false" :pattern="pattern"
                                    :data="treeData" key-field="id" label-field="name"
                                    @update:selected-keys="selectedTree">

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
                <n-card :segmented="{ content: true }" :bordered="false" size="small">
                    <template #header>
                        <n-space>
                            <n-icon size="18">
                                <FormOutlined />
                            </n-icon>
                            <span>编辑菜单{{ treeItemTitle ? `：${treeItemTitle} ` : '' }}</span>
                        </n-space>
                    </template>
                    <n-alert type="info" closable> 从菜单列表选择一项后，进行编辑</n-alert>
                    <n-form :model="formParams" :rules="rules" ref="formRef" label-placement="left" :label-width="100"
                        v-if="isEditMenu" class="py-4">
                        <n-form-item label="类型" path="type">
                            <span>{{ formParams.type === 1 ? '侧边栏菜单' : '' }}</span>
                        </n-form-item>
                        <n-form-item label="标题" path="label">
                            <n-input placeholder="请输入标题" v-model:value="formParams.label" />
                        </n-form-item>
                        <n-form-item label="副标题" path="subtitle">
                            <n-input placeholder="请输入副标题" v-model:value="formParams.subtitle" />
                        </n-form-item>
                        <n-form-item label="路径" path="path">
                            <n-input placeholder="请输入路径" v-model:value="formParams.path" />
                        </n-form-item>
                        <n-form-item label="打开方式" path="openType">
                            <n-radio-group v-model:value="formParams.openType" name="openType">
                                <n-space>
                                    <n-radio :value="1">当前窗口</n-radio>
                                    <n-radio :value="2">新窗口</n-radio>
                                </n-space>
                            </n-radio-group>
                        </n-form-item>
                        <n-form-item label="菜单权限" path="auth">
                            <n-input placeholder="请输入权限，多个权限用，分割" v-model:value="formParams.auth" />
                        </n-form-item>
                        <n-form-item path="auth" style="margin-left: 100px">
                            <n-space>
                                <n-button type="primary" :loading="subLoading" @click="formSubmit">保存修改</n-button>
                                <n-button @click="handleReset">重置</n-button>
                                <n-button @click="handleDel">删除</n-button>
                            </n-space>
                        </n-form-item>
                    </n-form>
                </n-card>
            </n-gi>
        </n-grid>

        <CreateDrawer ref="createDrawerRef" :title="drawerTitle" />
    </n-flex>
</template>
<script lang="ts" setup>
import { ref, unref, reactive, onMounted, computed, Ref, nextTick } from 'vue';
import { useDialog, useMessage } from 'naive-ui';
// import { DownOutlined, AlignLeftOutlined, SearchOutlined, FormOutlined } from '@vicons/antd';
// import { getMenuList } from '@/api/system/menu';
// import { getTreeItem } from '@/utils';
import CreateDrawer from './CreateDrawer.vue';
import { XNTree } from '@skit/x.naive-ui';
import { useColumns, useFormWrapper } from '@fast-crud/fast-crud';
import { equipment_api, fast_equipment_api } from './api'

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



function openCreateDrawer() {
    const { openDrawer } = createDrawerRef.value;
    openDrawer();
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
    let equipment_list = await equipment_api.list();
    const treeMenuList = generateTree(equipment_list.data.data);
    treeData.value = treeMenuList;
    loading.value = false;
}

function onTreeContainerResize({ width, height }) {
    treeHeight.value = height - 22;
}

onMounted(async () => {
    await refreshTree();

    nextTick(() => {
        if (treeContainer.value) {
            treeHeight.value = treeContainer.value.clientHeight - 22;
        }
    });

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
