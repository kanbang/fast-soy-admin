
import { el } from 'element-plus/es/locale';
import request from '/@/utils/request';

/**
 * 用户接口
 * @method getUserList 获取用户列表
 * @method allMenu 获取菜单接口，平铺
 * @method upsertMenu 更新保存菜单
 */


// https://stackoverflow.com/questions/41089854/typescript-access-static-attribute-of-generic-type

// class GenericClass<STR> {
//   s: string = STR.str;
// }

// class SS {
//   static str: string = "test";
// }

// class ChildClass extends GenericClass<SS> {
//   logstr() {
//     console.log(this.s);
//   }
// }


// export class FormSchemaApi extends CrudApi<FormSchemaApi> {
//   static __prefix: string = "form_schema";
// }


// new ChildClass().logstr()


export class CrudApi<T = object> {
    prefix: string;

    constructor(prefix: string) {
        this.prefix = prefix;
    }

    resHandle(res: any) {
        return res.data;
    }

    // Create One
    async create(data?: T) {
        const res = await request.post(`/${this.prefix}/create`, data);
        return this.resHandle(res);
    }


    // Delete By Key
    async delete(key?: number) {
        let params = new URLSearchParams();
        params.append('item_id', key);
        let str_params = params.toString();
        if (str_params.length > 0) {
            str_params = '?' + str_params;
        }

        const res = await request.post(`/${this.prefix}/delete/${str_params}`);
        return this.resHandle(res);
    }


    // Delete All
    async delete_all(data?: T) {
        const res = await request.post(`/${this.prefix}/delete_all`, data);
        return this.resHandle(res);
    }

    // Update One By Key
    async update(data?: T) {
        const res = await request.post(`/${this.prefix}/update`, data);
        return this.resHandle(res);
    }


    // Get One By Filter Value
    async get_by_id(data?: number|string) {
        const res = await request.post(`/${this.prefix}/get_by_id`, data);
        return this.resHandle(res);
    }


    // Get One By Filter Value
    async get_one_by_filter(data?: T, relationships: boolean | null = null, user_data_filter: boolean | null = null) {

        let params = new URLSearchParams();
        if (relationships !== null) params.append('relationships', relationships.toString());
        if (user_data_filter !== null) {
            if (user_data_filter)
                params.append('user_data_filter', 'SELF_DATA');
            else
                params.append('user_data_filter', 'ALL_DATA');
        }

        let str_params = params.toString();

        if (str_params.length > 0) {
            str_params = '?' + str_params;
        }

        const res = await request.post(`/${this.prefix}/get_one_by_filter${str_params}`, data);
        return this.resHandle(res);
    }


    // List All
    async list(sort_by: string | null = null, relationships: boolean | null = null, skip: number | null = null, limit: number | null = null, user_data_filter: boolean | null = null) {

        // 'http://localhost:8000/api/form_schema/list?sort_by=id&relationships=false&skip=0&limit=0' \

        // const params = new URLSearchParams(
        //   foo: 'bar',
        //   baz: 'boom',
        //   cow: 'milk',
        //   php: 'hypertext processor'
        // );

        let params = new URLSearchParams();
        if (sort_by !== null) params.append('sort_by', sort_by);
        if (relationships !== null) params.append('relationships', relationships.toString());
        if (skip !== null) params.append('skip', skip.toString());
        if (limit !== null) params.append('limit', limit.toString());
        if (user_data_filter !== null) {
            if (user_data_filter)
                params.append('user_data_filter', 'SELF_DATA');
            else
                params.append('user_data_filter', 'ALL_DATA');
        }

        let str = params.toString();

        if (str.length > 0) {
            str = '?' + str;
        }

        const res = await request.post(`/${this.prefix}/list${str}`);
        return this.resHandle(res);
    }


    // Query Many By Filter Value
    async query(data?: T) {
        const res = await request.post(`/${this.prefix}/query`, data);
        return this.resHandle(res);
    }


    // Query Many By Filter Condition, [=, !=, >, <, >=, <=, like, in]
    async query_ex(data?: T) {
        const res = await request.post(`/${this.prefix}/query_ex`, data);
        return this.resHandle(res);
    }


    // Insert Or Update
    async upsert(data?: T) {
        const res = await request.post(`/${this.prefix}/upsert`, data);
        return this.resHandle(res);
    }
}
