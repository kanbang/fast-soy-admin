import type { UserPageQuery } from '@fast-crud/fast-crud';
import { mockRequest } from '@/service/request';
import { CrudApi } from './crud-api';

const request = mockRequest;
// const apiPrefix = '/crud/demo';

export type DemoRecord = {
  id: number;
  [key: string]: any;
};



export class DummyApi extends CrudApi {
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

const dummy_api = new DummyApi();


export async function GetList(query: UserPageQuery) {
  return await dummy_api.list();
}

export async function AddObj(obj: DemoRecord) {
  return await dummy_api.create(obj);
}

export async function UpdateObj(obj: DemoRecord) {
  return await dummy_api.update(obj);
}

export async function DelObj(id: number) {
  return await dummy_api.delete(id);
}

export async function GetObj(id: number) {
  return await dummy_api.get_by_id(id);
}

export async function BatchDelete(ids: number[]) {
  // const res = await request.post(`${apiPrefix}/batchDelete`, { ids });
  // return resHandle(res);
}
