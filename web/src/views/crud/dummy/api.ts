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

type AnyObject = { [key: string]: any };

function removeEmptyValues(obj: AnyObject): AnyObject {
  const newObj: AnyObject = {};
  for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
          const value = obj[key];
          if (value !== null && value !== undefined && value !== "") {
              newObj[key] = value;
          }
      }
  }
  return newObj;
}

export async function GetList(query: UserPageQuery) {

  // page
  // {limit: 5, offset: 0}
  // query
  // {}
  // sort
  // Proxy(Object) {prop: 'age', order: false, asc: false}


  let params = new URLSearchParams();
  // if (sort_by !== null) params.append('sort_by', sort_by);
  // if (relationships !== null) params.append('relationships', relationships.toString());
  if (query.page.offset !== null) params.append('skip', query.page.offset.toString());
  if (query.page.limit !== null) params.append('limit', query.page.limit.toString());
  // if (user_data_filter !== null) {
  //     if (user_data_filter)
  //         params.append('user_data_filter', 'SELF_DATA');
  //     else
  //         params.append('user_data_filter', 'ALL_DATA');
  // }

  if (query.sort.prop && query.sort.order) {
    if (query.sort.asc) {
      params.append('sort_by', query.sort.prop);
    }
    else {
      params.append('sort_by', '-' + query.sort.prop);
    }
  }

  let str = params.toString();

  return await dummy_api.query(removeEmptyValues(query.query), str);
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
