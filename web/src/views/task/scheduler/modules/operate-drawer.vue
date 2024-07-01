<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue';
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
import { fetchAddUser, fetchGetRoleList, fetchUpdateUser } from '@/service/api';
import { $t } from '@/locales';

defineOptions({
  name: 'OperateDrawer'
});

interface Props {
  /** the type of operation */
  operateType: NaiveUI.TableOperateType;
  /** the edit row data */
  rowData?: any | null;
}

const props = defineProps<Props>();

interface Emits {
  (e: 'submitted'): void;
}

const emit = defineEmits<Emits>();

const visible = defineModel<boolean>('visible', {
  default: false
});

const { formRef, validate, restoreValidation } = useNaiveForm();
const { defaultRequiredRule } = useFormRules();

const title = computed(() => {
  const titles: Record<NaiveUI.TableOperateType, string> = {
    add: "添加任务",
    edit: "编辑任务"
  };
  return titles[props.operateType];
});

const model = reactive(createDefaultModel());

function createDefaultModel() {
  return {
    name: '',
    group: '',
    job_class: '',
    exec_strategy: '',
    expression: null,
    is_active: '',
    remark: '',
    start_date: null,
    end_date: null,
    create_datetime: null,
    update_datetime: null,
    last_run_datetime: null
  };
}

const taskGroupOptions = ref([])

const execStrategyOptions = ref([
  {
    value: "interval",
    label: "时间间隔(interval)"
  },

  {
    value: "cron",
    label: "Cron 表达式"
  },

  {
    value: "date",
    label: "指定日期时间(date)"
  }
])

type RuleKey = Extract<keyof Api.SystemManage.UserUpdateParams, 'userName' | 'password' | 'status'>;

const rules = ref<Record<RuleKey, App.Global.FormRule>>({

});

/** the enabled role options */
const roleOptions = ref<CommonType.Option<string>[]>([]);

async function getRoleOptions() {
  const { error, data } = await fetchGetRoleList({ status: '1' });

  if (!error) {
    const options = data.records.map(item => ({
      label: item.roleName,
      value: item.roleCode
    }));
    roleOptions.value = options;
  }
}

function handleInitModel() {
  Object.assign(model, createDefaultModel());

  if (props.operateType === 'edit' && props.rowData) {
    Object.assign(model, props.rowData);
  }

  if (props.operateType === 'add') {
    // rules.value.password.required = true;
  } else if (props.operateType === 'edit') {
    // rules.value.password.required = false;
  }
}

function closeDrawer() {
  visible.value = false;
}

async function handleSubmit() {
  await validate();
  // request

  if (props.operateType === 'add') {
    const { error } = await fetchAddUser(model);
    if (!error) {
      window.$message?.success($t('common.addSuccess'));
    }
  } else if (props.operateType === 'edit') {
    const { error } = await fetchUpdateUser(model);
    if (!error) {
      window.$message?.success($t('common.updateSuccess'));
    }
  }

  closeDrawer();
  emit('submitted');
}

watch(visible, () => {
  if (visible.value) {
    // debugger
    handleInitModel();
    restoreValidation();
    getRoleOptions();
  }
});
</script>

<template>
  <NDrawer v-model:show="visible" display-directive="show" :width="600">
    <NDrawerContent :title="title" :native-scrollbar="false" closable>
      <NForm ref="formRef" :model="model" :rules="rules">
        <n-grid :cols="24" :x-gap="24">
          <n-form-item-gi :span="24" :label="$t('任务名称')" path="name">
            <NInput v-model:value="model.name" :placeholder="$t('任务名称')" />
          </n-form-item-gi>
          <n-form-item-gi :span="24" :label="$t('任务分组')" path="group">
            <NSelect v-model:value="model.group" :options="taskGroupOptions" allow-create filterable
              default-first-option :placeholder="$t('请选择任务分组，支持直接输入添加')" />
          </n-form-item-gi>
          <n-form-item-gi :span="24" :label="$t('调用目标')" path="job_class">
            <NInput v-model:value="model.job_class"
              placeholder='调用示例：test.main.Test("kinit", 1314, True)；参数仅支持字符串，整数，浮点数，布尔类型。' />
          </n-form-item-gi>
          <n-form-item-gi :span="24" :label="$t('执行策略')" path="exec_strategy">
            <NRadioGroup v-model:value="model.exec_strategy">
              <NRadio v-for="item in execStrategyOptions" :key="item.value" :value="item.value" :label="item.label" />
            </NRadioGroup>
          </n-form-item-gi>
          <!-- <n-form-item-gi :span="24" v-if="model.exec_strategy === 'interval'" :label="$t('表达式')" path="expression">
            <NInput v-model:value="model.expression"
              :placeholder="$t('interval 表达式，五位，分别为：秒 分 时 天 周，例如：10 * * * * 表示每隔 10 秒执行一次任务。')" />
          </n-form-item-gi>
          <n-form-item-gi :span="24" v-if="model.exec_strategy === 'cron'" :label="$t('表达式')" path="expression">
            <NInput v-model:value="model.expression" :placeholder="$t('cron 表达式，六位或七位，分别表示秒、分钟、小时、天、月、星期几、年(可选)')" />
          </n-form-item-gi>
          <n-form-item-gi :span="24" v-if="model.exec_strategy === 'date'" :label="$t('执行时间')" path="expression">
            <NDatePicker v-model:value="model.expression" type="datetime" format="YYYY-MM-DD HH:mm:ss"
              value-format="YYYY-MM-DD HH:mm:ss" />
          </n-form-item-gi> -->
          <n-form-item-gi :span="12" v-if="model.exec_strategy !== 'date'" :label="$t('开始时间')" path="start_date">
            <NDatePicker v-model:value="model.start_date" type="datetime" format="YYYY-MM-DD HH:mm:ss"
              value-format="YYYY-MM-DD HH:mm:ss" />
          </n-form-item-gi>
          <n-form-item-gi :span="12" v-if="model.exec_strategy !== 'date'" :label="$t('结束时间')" path="end_date">
            <NDatePicker v-model:value="model.end_date" type="datetime" format="YYYY-MM-DD HH:mm:ss"
              value-format="YYYY-MM-DD HH:mm:ss" />
          </n-form-item-gi>
          <n-form-item-gi :span="12" :label="$t('任务状态')" path="is_active">
            <NRadioGroup v-model:value="model.is_active">
              <NRadio value="true" :label="$t('正常')" />
              <NRadio value="false" :label="$t('停用')" />
            </NRadioGroup>
          </n-form-item-gi>

          <n-form-item-gi :span="12" :label="$t('')" path="">
            <span>{{ $t('创建或更新任务完成后，如果任务状态与设置的不符，请尝试刷新数据或查看调度日志，任务状态可能会有延迟(几秒)。') }}</span>
          </n-form-item-gi>
          <n-form-item-gi :span="24" :label="$t('备注说明')" path="remark">
            <NInput v-model:value="model.remark" type="textarea" :placeholder="$t('备注说明')" maxlength="1000"
              show-word-limit rows="3" />
          </n-form-item-gi>
        </n-grid>
      </NForm>
      <template #footer>
        <NSpace :size="16">
          <NButton @click="closeDrawer">{{ $t('common.cancel') }}</NButton>
          <NButton type="primary" @click="handleSubmit">{{ $t('common.confirm') }}</NButton>
        </NSpace>
      </template>
    </NDrawerContent>
  </NDrawer>
</template>

<style scoped></style>
