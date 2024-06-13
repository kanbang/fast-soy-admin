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

export class MfptApi extends CrudApi<MfptApi> {
  constructor() {
    super("mfpt");
  }
}

export const mfpt_api = MfptApi.instance();
export const fast_mfpt_api = new FastCrudApi(mfpt_api);

//////////////////////////////////////////////////////////////////////
export class MfpApi extends CrudApi<MfpApi> {
  constructor() {
    super("mfp");
  }
}

export const mfp_api = MfpApi.instance();
export const fast_mfp_api = new FastCrudApi(mfp_api);


