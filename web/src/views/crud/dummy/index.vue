<template>
  <div class="h-full">
    <fs-crud ref="crudRef" v-bind="crudBinding"> </fs-crud>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { CreateCrudOptionsProps, CreateCrudOptionsRet, ValueBuilderContext, useFs } from "@fast-crud/fast-crud";
import type { AddReq, DelReq, EditReq, UserPageQuery, UserPageRes, ValueResolveContext } from '@fast-crud/fast-crud';
import { dict } from '@fast-crud/fast-crud';
import dayjs from 'dayjs';
import { fast_dummy_api } from './api';

function createCrudOptions({ crudExpose }: CreateCrudOptionsProps): CreateCrudOptionsRet {
  const pageRequest = async (query: UserPageQuery): Promise<UserPageRes> => {
    return fast_dummy_api.GetList(query);
  };
  const editRequest = async (ctx: EditReq) => {
    const { form, row } = ctx;
    form.id = row.id;
    return fast_dummy_api.UpdateObj(form);
  };
  const delRequest = async (ctx: DelReq) => {
    const { row } = ctx;
    return fast_dummy_api.DelObj(row.id);
  };

  const addRequest = async (req: AddReq) => {
    const { form } = req;
    return fast_dummy_api.AddObj(form);
  };

  return {
    crudOptions: {
      container: {
        is: 'fs-layout-card'
      },
      request: {
        pageRequest,
        addRequest,
        editRequest,
        delRequest
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
          title: '姓名',
          type: 'text',
          search: { show: true },
          column: {
            sorter: 'custom',
          }
        },
        age: {
          title: '年龄',
          type: 'number',
          column: {
            sorter: 'custom',
            width: 50
          },
          form: {
            show: true
          }
        },
        salary: {
          title: '薪水',
          type: 'number',
          column: {
            width: 50
          },
          form: {
            show: true
          }
        },
        is_active: {
          title: '启用',
          type: 'dict-switch',
          column: {
            width: 50
          },
          form: {
            show: true
          }
        },
        birthdate: {
          title: '生日',
          type: 'date',
         
          valueBuilder(context) {
            const { value, row, key } = context;
            if (value) {
              row[key] = dayjs(value).valueOf();
            }
          },
          valueResolve(context) {
            const { value, form, key } = context;
            if (value) {
              form[key] = dayjs(value).format('YYYY-MM-DD');
            }
          }
        },
        created_at: {
          title: '创建时间',
          type: 'datetime',
          valueBuilder(context) {
            const { value, row, key } = context;
            if (value) {
              row[key] = dayjs(value).valueOf();
            }
          },
          valueResolve(context) {
            const { value, form, key } = context;
            if (value) {
              form[key] = dayjs(value).format('YYYY-MM-DD HH:mm:ss');
            }
          }
        },
     
        notes: {
          title: '文本',
          type: 'text',
          search: { show: true }
        },

        json_data: {
          title: 'json',
          type: 'json',
          form: {
            valueBuilder({ form }: ValueBuilderContext) {
              if (form.json == null) {
                return;
              }
              form.json = JSON.parse(form.json);
            },
            valueResolve({ form }: ValueResolveContext) {
              if (form.json == null) {
                return;
              }
              form.json = JSON.stringify(form.json);
            },
          },
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
