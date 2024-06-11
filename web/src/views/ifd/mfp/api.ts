/*
 * @Descripttion: 
 * @version: 0.x
 * @Author: zhai
 * @Date: 2024-06-09 13:24:29
 * @LastEditors: zhai
 * @LastEditTime: 2024-06-10 19:46:31
 */

import { mockRequest, request } from '@/service/request';
import { CrudApi } from '@/service/crud-api';
import { FastCrudApi } from '@/service/fast-crud-api';

export class MfstApi extends CrudApi<MfstApi> {
  constructor() {
    super("mfst");
  }
}

export const mfst_api = MfstApi.instance();
export const fast_mfst_api = new FastCrudApi(mfst_api);

//////////////////////////////////////////////////////////////////////
export class MfsApi extends CrudApi<MfsApi> {
  constructor() {
    super("mfs");
  }
}

export const mfs_api = MfsApi.instance();
export const fast_mfs_api = new FastCrudApi(mfs_api);


