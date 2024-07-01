<!--
 * @Descripttion: 
 * @version: 0.x
 * @Author: zhai
 * @Date: 2024-06-29 10:21:23
 * @LastEditors: zhai
 * @LastEditTime: 2024-06-29 16:55:57
-->
<script setup lang="ts">
import { computed } from 'vue';
import { $t } from '@/locales';
import { useFormRules, useNaiveForm } from '@/hooks/common/form';
import { enableStatusOptions, userGenderOptions } from '@/constants/business';
import { translateOptions } from '@/utils/common';

defineOptions({
  name: 'Search'
});

interface Emits {
  (e: 'reset'): void;
  (e: 'search'): void;
}

const emit = defineEmits<Emits>();

const { formRef, validate, restoreValidation } = useNaiveForm();

const model = defineModel<Api.SystemManage.UserSearchParams>('model', { required: true });

type RuleKey = Extract<keyof Api.SystemManage.UserSearchParams, 'userEmail' | 'userPhone'>;

const rules = computed<Record<RuleKey, App.Global.FormRule>>(() => {
  const { patternRules } = useFormRules(); // inside computed to make locale reactive

  return {
    userEmail: patternRules.email,
    userPhone: patternRules.phone
  };
});

async function reset() {
  await restoreValidation();
  emit('reset');
}

async function search() {
  await validate();
  emit('search');
}
</script>

<template>
  <NCard :title="$t('common.search')" :bordered="false" size="small" class="card-wrapper">
    <NForm ref="formRef" :model="model" :rules="rules" label-placement="left" :label-width="70">
      <NGrid :cols="24" :x-gap="24" responsive="screen" item-responsive>
        <NFormItemGi span="24 s:12 m:6" label="任务名称" path="name" class="pr-24px">
          <NInput v-model:value="model.name" placeholder="请输入任务名称" />
        </NFormItemGi>
        <NFormItemGi span="24 s:12 m:6" label="任务编号" path="id" class="pr-24px">
          <NInput v-model:value="model.id" placeholder="请输入任务编号" />
        </NFormItemGi>
        <NFormItemGi span="24 s:12 m:6" label="任务分组" path="group" class="pr-24px">
          <NSelect v-model:value="model.group" placeholder="请选择任务编号" :options="translateOptions(userGenderOptions)"
            clearable />
        </NFormItemGi>

        <NFormItemGi span="24 s:12 m:6">
          <NSpace class="w-full" justify="end">
            <NButton @click="reset">
              <template #icon>
                <icon-ic-round-refresh class="text-icon" />
              </template>
              {{ $t('common.reset') }}
            </NButton>
            <NButton type="primary" ghost @click="search">
              <template #icon>
                <icon-ic-round-search class="text-icon" />
              </template>
              {{ $t('common.search') }}
            </NButton>
          </NSpace>
        </NFormItemGi>
      </NGrid>
    </NForm>
  </NCard>
</template>

<style scoped></style>
