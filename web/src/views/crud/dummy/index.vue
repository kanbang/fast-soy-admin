<template>
  <div class="h-full">
    <fs-crud ref="crudRef" v-bind="crudBinding"> </fs-crud>
  </div>
</template>

<script setup lang="ts">
import {onMounted, ref} from "vue";
import {CreateCrudOptionsProps, CreateCrudOptionsRet,   ValueBuilderContext, useFs} from "@fast-crud/fast-crud";
import type { AddReq, DelReq, EditReq, UserPageQuery, UserPageRes } from '@fast-crud/fast-crud';
import { dict } from '@fast-crud/fast-crud';
import dayjs from 'dayjs';
import * as api from './api';

function createCrudOptions({crudExpose}: CreateCrudOptionsProps): CreateCrudOptionsRet {
  const pageRequest = async (query: UserPageQuery): Promise<UserPageRes> => {
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
    return api.AddObj(form);
  };


  // "name": "string",
  // "age": 0,
  // "salary": 0,
  // "is_active": true,
  // "birthdate": "2024-06-04",
  // "created_at": "2024-06-04T06:46:56.703Z",
  // "notes": "string",
  // "json_data": "string"

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
          // naive 默认仅支持数字类型时间戳作为日期输入与输出
          // 字符串类型的时间需要转换格式
          valueBuilder(context) {
            const { value, row, key } = context;
            if (value) {
              // naive 默认仅支持时间戳作为日期输入与输出
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
          // naive 默认仅支持数字类型时间戳作为日期输入与输出
          // 字符串类型的时间需要转换格式
          valueBuilder(context) {
            const { value, row, key } = context;
            if (value) {
              // naive 默认仅支持时间戳作为日期输入与输出
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
        // select: {
        //   title: '状态',
        //   search: { show: true },
        //   type: 'dict-select',
        //   dict: dict({
        //     url: '/mock/crud/demo/dict'
        //   })
        // },
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

        // copyable: {
        //   title: '可复制',
        //   type: ['text', 'copyable'],
        //   search: { show: true }
        // },
        // avatar: {
        //   title: '头像裁剪',
        //   type: 'cropper-uploader'
        // },
        // upload: {
        //   title: '文件上传',
        //   type: 'file-uploader'
        // },
        // richtext: {
        //   title: '富文本',
        //   type: 'editor-wang5',
        //   column: {
        //     // cell中不显示
        //     show: false
        //   },
        //   form: {
        //     col: {
        //       // 横跨两列
        //       span: 24
        //     },
        //     component: {
        //       style: {
        //         height: '300px'
        //       }
        //     }
        //   }
        // }
      }
    }
  };
}

const {crudRef, crudBinding, crudExpose} = useFs({createCrudOptions});

// 页面打开后获取列表数据
onMounted(() => {
  crudExpose.doRefresh();
});

</script>




