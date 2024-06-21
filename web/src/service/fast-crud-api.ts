import type { UserPageQuery } from '@fast-crud/fast-crud';
import { CrudApi, Singleton } from './crud-api';


type DictObject = { [key: string]: any };

function removeEmptyValues(obj: DictObject): DictObject {
    const newObj: DictObject = {};
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



export class FastCrudApi<CLS, T = object | undefined> extends CrudApi<CLS> {

    constructor(prefix: string) {
        super(prefix);
    }

    async GetList(query: UserPageQuery) {

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

        return await this.query(removeEmptyValues(query.query), str);
    }

    async AddObj(obj: T) {
        return await this.create(obj);
    }

    async UpdateObj(obj: T) {
        return await this.update(obj);
    }

    async DelObj(id: number) {
        return await this.delete(id);
    }

    async GetObj(id: number) {
        return await this.get_by_id(id);
    }

    async BatchDelete(ids: number[]) {
        // const res = await request.post(`${apiPrefix}/batchDelete`, { ids });
        // return resHandle(res);
    }
}
