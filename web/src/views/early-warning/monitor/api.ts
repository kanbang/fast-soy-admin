/*
 * @Descripttion: 
 * @version: 0.x
 * @Author: zhai
 * @Date: 2024-06-09 13:24:29
 * @LastEditors: zhai
 * @LastEditTime: 2024-06-10 20:01:08
 */

import { mockRequest, request } from '@/service/request';
import { CrudApi } from '@/service/crud-api';
import { FastCrudApi } from '@/service/fast-crud-api';

export class EquipmentApi extends CrudApi<EquipmentApi> {
  constructor() {
    super("equipment");
  }
}

export const equipment_api = EquipmentApi.instance();

export const fast_equipment_api = new FastCrudApi(equipment_api);


