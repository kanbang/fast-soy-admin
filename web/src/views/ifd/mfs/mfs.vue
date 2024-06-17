<!--
 * @Descripttion: 
 * @version: 0.x
 * @Author: zhai
 * @Date: 2024-06-10 19:30:05
 * @LastEditors: zhai
 * @LastEditTime: 2024-06-10 22:17:59
-->
<template>
  <div class="h-full">
    <n-alert v-if="props.type_id == null" type="info" closable>
      从类型列表选择一项后，进行编辑
    </n-alert>
    <fs-crud v-else ref="crudRef" v-bind="crudBinding"> </fs-crud>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { CreateCrudOptionsProps, CreateCrudOptionsRet, ValueBuilderContext, useFs } from "@fast-crud/fast-crud";
import type { AddReq, DelReq, EditReq, UserPageQuery, UserPageRes, ValueResolveContext } from '@fast-crud/fast-crud';
import { dict } from '@fast-crud/fast-crud';
import dayjs from 'dayjs';
import { fast_mfs_api as api } from './api';


interface Props {
  type_id: number | null;
}

const props = withDefaults(defineProps<Props>(), {
  type_id: null
});


watch(() => props.type_id,
  () => {
    crudExpose.doRefresh();
  });

function createCrudOptions({ crudExpose }: CreateCrudOptionsProps): CreateCrudOptionsRet {
  const pageRequest = async (query: UserPageQuery): Promise<UserPageRes> => {
    query.query['type_id'] = props.type_id;
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
    form['type_id'] = props.type_id;
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
      rowHandle: {
        width: 150
      },
      search: {
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
            width: 50
          },
          form: {
            show: false
          }
        },
        name: {
          title: '名称',
          type: 'text',
          search: { show: true },
          column: {
            sorter: 'custom',
          }
        },

        desc: {
          title: '描述',
          type: 'text',
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

</script>
