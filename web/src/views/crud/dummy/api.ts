/*
 * @Descripttion: 
 * @version: 0.x
 * @Author: zhai
 * @Date: 2024-06-05 21:21:25
 * @LastEditors: zhai
 * @LastEditTime: 2024-06-09 15:44:45
 */
import { mockRequest, request } from '@/service/request';
import { CrudApi } from '@/service/crud-api';
import { FastCrudApi } from '@/service/fast-crud-api';

export class DummyApi extends CrudApi<DummyApi> {
  constructor() {
    super("dummy");
  }

  export_csv(id?: string) {
    return request({
      url: `/${this.prefix}/export_csv/${id}`,
      method: 'GET',
      responseType: "blob"
    });
  }
}

export const dummy_api = DummyApi.instance();

export type DemoRecord = {
  id: number;
  [key: string]: any;
};

export const fast_dummy_api = FastCrudApi.instance(dummy_api) as FastCrudApi<DemoRecord>;
