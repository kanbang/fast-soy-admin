<template>
    <div>
        <div class="n-layout-page-header">
            <n-card :bordered="false" title="菜单权限管理">
                页面数据为 Mock 示例数据，非真实数据。
            </n-card>
        </div>
        <n-grid class="mt-4" cols="1 s:1 m:1 l:3 xl:3 2xl:3" responsive="screen" :x-gap="12">
            <n-gi span="1">
                <n-card :segmented="{ content: true }" :bordered="false" size="small">
                    <template #header>
                        <n-space>
                            <n-dropdown trigger="hover" @select="selectAddMenu" :options="addMenuOptions">
                                <n-button type="info" ghost icon-placement="right">
                                    添加菜单
                                    <template #icon>
                                        <div class="flex items-center">
                                            <n-icon size="14">
                                                <DownOutlined />
                                            </n-icon>
                                        </div>
                                    </template>
                                </n-button>
                            </n-dropdown>
                            <n-button type="info" ghost icon-placement="left" @click="packHandle">
                                全部{{ expandedKeys.length ? '收起' : '展开' }}
                                <template #icon>
                                    <div class="flex items-center">
                                        <n-icon size="14">
                                            <AlignLeftOutlined />
                                        </n-icon>
                                    </div>
                                </template>
                            </n-button>
                        </n-space>
                    </template>
                    <div class="w-full menu">
                        <n-input type="input" v-model:value="pattern" placeholder="输入菜单名称搜索">
                            <template #suffix>
                                <n-icon size="18" class="cursor-pointer">
                                    <SearchOutlined />
                                </n-icon>
                            </template>
                        </n-input>
                        <div class="py-3 menu-list">
                            <template v-if="loading">
                                <div class="flex items-center justify-center py-4">
                                    <n-spin size="medium" />
                                </div>
                            </template>
                            <template v-else>
                                <x-n-tree block-line cascade :virtual-scroll="true" :pattern="pattern" :data="treeData" key-field="id"
                                    :expandedKeys="expandedKeys" style="max-height: 650px; overflow: hidden"
                                    @update:selected-keys="selectedTree" @update:expanded-keys="onExpandedKeys">

                                    <template #render-label="{ option }">
                                        <span class="custom-tree-node">
                                            <span>{{ option.label }}</span>
                                            <span>
                                                <n-button @click="addChildNode(option)" ghost size="small" type="info">
                                                    添加子节点
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
            <n-gi span="2">
                <n-card :segmented="{ content: true }" :bordered="false" size="small">
                    <template #header>
                        <n-space>
                            <n-icon size="18">
                                <FormOutlined />
                            </n-icon>
                            <span>编辑菜单{{ treeItemTitle ? `：${treeItemTitle}` : '' }}</span>
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
    </div>
</template>
<script lang="ts" setup>
import { ref, unref, reactive, onMounted, computed } from 'vue';
import { useDialog, useMessage } from 'naive-ui';
// import { DownOutlined, AlignLeftOutlined, SearchOutlined, FormOutlined } from '@vicons/antd';
// import { getMenuList } from '@/api/system/menu';
// import { getTreeItem } from '@/utils';
import CreateDrawer from './CreateDrawer.vue';
import { XNTree } from '@skit/x.naive-ui';

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

const isAddSon = computed(() => {
    return !treeItemKey.value.length;
});

const addMenuOptions = ref([
    {
        label: '添加顶级菜单',
        key: 'home',
        disabled: false,
    },
    {
        label: '添加子菜单',
        key: 'son',
        disabled: isAddSon,
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


const mlist: any[] = [
    {
        label: 'Dashboard',
        key: 'dashboard',
        type: 1,
        subtitle: 'dashboard',
        openType: 1,
        auth: 'dashboard',
        path: '/dashboard',
        children: [
            {
                label: '主控台',
                key: 'console',
                type: 1,
                subtitle: 'console',
                openType: 1,
                auth: 'console',
                path: '/dashboard/console',
            },
            {
                label: '工作台',
                key: 'workplace',
                type: 1,
                subtitle: 'workplace',
                openType: 1,
                auth: 'workplace',
                path: '/dashboard/workplace',
            },
        ],
    },
    {
        label: '表单管理',
        key: 'form',
        type: 1,
        subtitle: 'form',
        openType: 1,
        auth: 'form',
        path: '/form',
        children: [
            {
                label: '基础表单',
                key: 'basic-form',
                type: 1,
                subtitle: 'basic-form',
                openType: 1,
                auth: 'basic-form',
                path: '/form/basic-form',
            },
            {
                label: '分步表单',
                key: 'step-form',
                type: 1,
                subtitle: 'step-form',
                openType: 1,
                auth: 'step-form',
                path: '/form/step-form',
            },
            {
                label: '表单详情',
                key: 'detail',
                type: 1,
                subtitle: 'detail',
                openType: 1,
                auth: 'detail',
                path: '/form/detail',
            },
        ],
    },
];

function addChildNode(option: any) {
    console.log(option)
}


function delNode(option: any) {
    console.log(option)
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


function selectAddMenu(key: string) {
    drawerTitle.value = key === 'home' ? '添加顶栏菜单' : `添加子菜单：${treeItemTitle.value}`;
    openCreateDrawer();
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

function packHandle() {
    if (expandedKeys.value.length) {
        expandedKeys.value = [];
    } else {
        expandedKeys.value = unref(treeData).map((item: any) => item.key as string) as [];
    }
}


function createData(level = 4, baseKey = ''): TreeOption[] | undefined {
    if (!level) return undefined
    return repeat(6 - level, undefined).map((_, index) => {
        const key = '' + baseKey + level + index
        const label = createLabel(level)
        return {
            label,
            key,
            children: createData(level - 1, key),
            suffix: () =>
                h(
                    NButton,
                    { text: true, type: 'primary' },
                    { default: () => 'Suffix' }
                ),
            prefix: () =>
                h(NButton, { text: true, type: 'primary' }, { default: () => 'Prefix' })
        }
    })
}

onMounted(async () => {
    const treeMenuList = mlist;
    const keys = treeMenuList.map((item) => item.key);
    Object.assign(formParams, keys);
    treeData.value = treeMenuList;
    loading.value = false;
});

function onExpandedKeys(keys) {
    expandedKeys.value = keys;
}
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
