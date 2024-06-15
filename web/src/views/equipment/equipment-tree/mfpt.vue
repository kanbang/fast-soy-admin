<!--
 * @Descripttion: 
 * @version: 0.x
 * @Author: zhai
 * @Date: 2024-06-10 19:30:05
 * @LastEditors: zhai
 * @LastEditTime: 2024-06-15 20:35:48
-->
<template>
  <div class="h-full">
    <fs-crud ref="crudRef" v-bind="crudBinding"> </fs-crud>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { CreateCrudOptionsProps, CreateCrudOptionsRet, ValueBuilderContext, useFs } from "@fast-crud/fast-crud";
import type { AddReq, DelReq, EditReq, UserPageQuery, UserPageRes, ValueResolveContext } from '@fast-crud/fast-crud';
import { fast_mfpt_api as api } from '@/views/ifd/mfp/api';


interface Props {
  selkeys: Array<number>;
}

const props = withDefaults(defineProps<Props>(), {
  selkeys: []
});

// 初始化响应式状态
const selectedRowKeys = ref(props.selkeys);

// 监听props.selkeys
watch(() => props.selkeys, (newVal) => {
  selectedRowKeys.value = newVal;
});

const emit = defineEmits<{
  (e: 'select-types', value: Array<number>): void;
}>();


function createCrudOptions({ crudExpose }: CreateCrudOptionsProps): CreateCrudOptionsRet {
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
      settings: {
        plugins: {
          //这里使用行选择插件，生成行选择crudOptions配置，最终会与crudOptions合并
          rowSelection: {
            enabled: true,
            order: -2,
            before: true,
            // handle: (pluginProps,useCrudProps)=>CrudOptions,
            props: {
              multiple: true,
              crossPage: true,
              selectedRowKeys,
              onSelectedChanged(selected) {
                // props.selkeys.value = selected;
                if (selected?.length > 0) {
                  emit('select-types', selected);
                }
                else {
                  emit('select-types', []);
                }

                console.log("已选择变化：", selected);
              }
            }
          }
        }
      },
      table: {
        striped: true
      },
      toolbar: {
        show: false,
      },
      actionbar: {
        show: false,
      },
      rowHandle: {
        show: false,
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
            show: false,
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
