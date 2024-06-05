<template>
  <div class="h-full">
    <fs-crud ref="crudRef" v-bind="crudBinding"> </fs-crud>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { CreateCrudOptionsProps, CreateCrudOptionsRet, useFs } from "@fast-crud/fast-crud";
import type { AddReq, DelReq, EditReq, UserPageQuery, UserPageRes } from '@fast-crud/fast-crud';
import { dict } from '@fast-crud/fast-crud';
import dayjs from 'dayjs';
import * as api from './api';

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

        unitid: {
          title: '机组ID',
          type: 'text',
          column: {
            // width: 50
          }
        },
        name: {
          title: '机组名称',
          type: 'text',
          column: {
            // width: 50
          }
        },
        code: {
          title: '机组编码',
          type: 'text',
          column: {
            // width: 50
          }
        },
        group: {
          title: '所属集团',
          type: 'text',
          column: {
            // width: 50
          }
        },
        plant: {
          title: '所属电厂',
          type: 'text',
          column: {
            // width: 50
          }
        },
        power: {
          title: '机组功率',
          type: 'text',
          column: {
            // width: 50
          }
        },
        type: {
          title: '型号',
          type: 'text',
          column: {
            // width: 50
          }
        },
        axis_code: {
          title: '轴系编码',
          type: 'text',
          column: {
            // width: 50
          }
        },
        axis_catalog: {
          title: '轴系目录',
          type: 'text',
          column: {
            // width: 50
          }
        },
        tsi: {
          title: 'TSI配置',
          type: 'text',
          column: {
            // width: 50
          }
        },
        tdm: {
          title: 'TDM配置',
          type: 'text',
          column: {
            // width: 50
          }
        },
        manufacturer: {
          title: '制造厂商',
          type: 'text',
          column: {
            // width: 50
          }
        },
        cooling: {
          title: '冷凝方式',
          type: 'text',
          column: {
            // width: 50
          }
        },
        gen_cooling: {
          title: '发电机冷却方式',
          type: 'text',
          column: {
            // width: 50
          }
        },
        heat_supply: {
          title: '是否供热',
          type: 'dict-switch',
          column: {
            // width: 50
          }
        },
        last_overhaul: {
          title: '最后一次大修时间',
          type: 'date',
          column: {
            // width: 50
          },
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
        info_update: {
          title: '信息更新时间',
          type: 'date',
          column: {
            // width: 50
          },
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
        rod_start: {
          title: '投产时间',
          type: 'date',
          column: {
            // width: 50
          },
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
        mfg_date: {
          title: '制造日期',
          type: 'date',
          column: {
            // width: 50
          },
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
        install_desc: {
          title: '安装过程描述',
          type: 'text',
          column: {
            // width: 50
          }
        },
        crit_speed: {
          title: '临界转速',
          type: 'text',
          column: {
            // width: 50
          }
        },

        // unitid = fields.CharField(max_length=255, null=False)
        // name = fields.CharField(max_length=255, null=False)
        // code = fields.CharField(max_length=255, null=False)
        // group = fields.CharField(max_length=255, description="集团")
        // plant = fields.CharField(max_length=255, description="电厂")
        // power = fields.CharField(max_length=255, description="功率")
        // type = fields.CharField(max_length=255, description="型号")
        // axis_code = fields.CharField(max_length=255, description="轴系编码")
        // axis_catalog = fields.CharField(max_length=255, description="轴系目录")
        // tsi = fields.CharField(max_length=255, description="TSI配置")
        // tdm = fields.CharField(max_length=255, description="TDM配置")
        // manufacturer = fields.CharField(max_length=255, description="制造厂商")
        // cooling = fields.CharField(max_length=255, description="冷凝方式")
        // gen_cooling = fields.CharField(max_length=255, description="发电机冷却方式")
        // heat_supply = fields.BooleanField(default=False, description="是否供热")
        // last_overhaul = fields.DateField(description="最后一次大修时间")
        // info_update = fields.DateField(description="信息更新时间")
        // rod_start = fields.DateField(description="投产时间")
        // mfg_date = fields.DateField(description="制造日期")
        // install_desc = fields.TextField(description="安装过程描述")
        // crit_speed = fields.FloatField(description="临界转速")


        // datetime: {
        //   title: '时间',
        //   type: 'datetime',
        //   // naive 默认仅支持数字类型时间戳作为日期输入与输出
        //   // 字符串类型的时间需要转换格式
        //   valueBuilder(context) {
        //     const { value, row, key } = context;
        //     if (value) {
        //       // naive 默认仅支持时间戳作为日期输入与输出
        //       row[key] = dayjs(value).valueOf();
        //     }
        //   },
        //   valueResolve(context) {
        //     const { value, form, key } = context;
        //     if (value) {
        //       form[key] = dayjs(value).format('YYYY-MM-DD HH:mm:ss');
        //     }
        //   }
        // },
        // select: {
        //   title: '状态',
        //   search: { show: true },
        //   type: 'dict-select',
        //   dict: dict({
        //     url: '/mock/crud/demo/dict'
        //   })
        // },
        // text: {
        //   title: '文本',
        //   type: 'text',
        //   search: { show: true }
        // },
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

const { crudRef, crudBinding, crudExpose } = useFs({ createCrudOptions });

// 页面打开后获取列表数据
onMounted(() => {
  crudExpose.doRefresh();
});

</script>
