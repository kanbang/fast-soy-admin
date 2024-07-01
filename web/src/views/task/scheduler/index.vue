<script setup lang="tsx">
import { NButton, NPopconfirm, NTag } from 'naive-ui';
import { fetchBatchDeleteUser, fetchDeleteUser, fetchGetUserList, fetchGetTaskList } from '@/service/api';
import { $t } from '@/locales';
import { useAppStore } from '@/store/modules/app';
import { enableStatusRecord, userGenderRecord } from '@/constants/business';
import { useTable, useTableOperate } from '@/hooks/common/table';
import OperateDrawer from './modules/operate-drawer.vue';
import Search from './modules/search.vue';

const appStore = useAppStore();

const { columns, columnChecks, data, getData, loading, mobilePagination, searchParams, resetSearchParams } = useTable({
  apiFn: fetchGetTaskList,
  showTotal: true,
  apiParams: {
    current: 1,
    size: 10,
    // if you want to use the searchParams in Form, you need to define the following properties, and the value is null
    // the value can not be undefined, otherwise the property in Form will not be reactive
    status: null,
    userName: null,
    password: null,
    userGender: null,
    nickName: null,
    userPhone: null,
    userEmail: null
  },
  columns: () => [
    {
      key: 'id',
      title: 'ID',
      align: 'center',
      width: '40px'
    },
    {
      key: 'name',
      title: '任务名称',
      align: 'center',
      minWidth: 100
    },
    {
      key: 'group',
      title: '任务分组',
      align: 'center',
      minWidth: 80
    },
    {
      key: 'job_class',
      title: '调用目标',
      align: 'center',
      minWidth: 100
    },
    {
      key: 'exec_strategy',
      title: '执行策略',
      align: 'center',
      minWidth: 70,
      render: row => (
        <NTag>
          {row.exec_strategy}
        </NTag>
      )
    },
    {
      key: 'expression',
      title: '表达式',
      align: 'center',
      minWidth: 100
    },
    {
      key: 'is_active',
      title: '状态',
      align: 'center',
      width: '80px',
      render: row => (
        <NSwitch value={row.is_active} disabled />
      )
    },
    {
      key: 'last_run_datetime',
      title: '最近执行时间',
      align: 'center',
      width: '110px'
    },
    {
      key: 'remark',
      title: '备注',
      align: 'center',
      minWidth: 60
    },
    {
      key: 'create_datetime',
      title: '创建时间',
      align: 'center',
      width: '100px'
    },
    {
      key: 'operate',
      title: '操作',
      align: 'center',
      width: '280px',
      render: row => (
        <div class="flex-center gap-8px">
          <NButton type="primary" ghost size="small" onClick={() => edit(row.id)}>
            编辑
          </NButton>
          <NButton type="primary" ghost size="small" onClick={() => toRecord(row)}>
            日志
          </NButton>
          <NButton type="primary" ghost size="small" onClick={() => runOnceTask(row)}>
            执行一次
          </NButton>
          <NPopconfirm onPositiveClick={() => delData(row)}>
            {{
              trigger: () => (
                <NButton type="error" ghost size="small">
                  删除
                </NButton>
              ),
              default: () => '是否确认删除？'
            }}
          </NPopconfirm>
        </div>
      )
    }
  ]
});

const {
  drawerVisible,
  operateType,
  editingData,
  handleAdd,
  handleEdit,
  checkedRowKeys,
  onBatchDeleted,
  onDeleted
  // closeDrawer
} = useTableOperate(data, getData);

async function handleBatchDelete() {
  // request
  const { error } = await fetchBatchDeleteUser({ ids: checkedRowKeys.value });
  if (!error) {
    onBatchDeleted();
  }
}

async function handleDelete(id: number) {
  // request
  const { error } = await fetchDeleteUser({ id });
  if (!error) {
    onDeleted();
  }
}

function edit(id: number) {
  handleEdit(id);
}
</script>

<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <Search v-model:model="searchParams" @reset="resetSearchParams" @search="getData" />
    <NCard title="定时任务列表" :bordered="false" size="small" class="sm:flex-1-hidden card-wrapper">
      <template #header-extra>
        <TableHeaderOperation v-model:columns="columnChecks" :disabled-delete="checkedRowKeys.length === 0"
          :loading="loading" @add="handleAdd" @delete="handleBatchDelete" @refresh="getData">

          <template #default>
            <NButton size="small" ghost type="primary" @click="handleAdd">
              <template #icon>
                <icon-ic-round-plus class="text-icon" />
              </template>
              添加
            </NButton>
            <NButton size="small" ghost type="primary" @click="handleRefreshAPI">
              <template #icon>
                <icon-radix-icons:magic-wand class="text-icon" />
              </template>
              生成Cron表达式
            </NButton>
            <span></span>
          </template>
        </TableHeaderOperation>

      </template>
      <NDataTable v-model:checked-row-keys="checkedRowKeys" :columns="columns" :data="data" size="small"
        :flex-height="!appStore.isMobile" :scroll-x="962" :loading="loading" remote :row-key="row => row.id"
        :pagination="mobilePagination" class="sm:h-full" striped :single-line="false" />
      <OperateDrawer v-model:visible="drawerVisible" :operate-type="operateType" :row-data="editingData"
        @submitted="getData" />
    </NCard>
  </div>
</template>

<style scoped></style>
