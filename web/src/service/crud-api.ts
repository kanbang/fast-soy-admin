
import { request } from '@/service/request';



export class Singleton<T> {
    private static __instances: Map<string, any> = new Map();

    static instance<T>(this: new (...args: any[]) => T, ...args: any[]): T {
        const className = this.name;
        if (!Singleton.__instances.has(className)) {
            Singleton.__instances.set(className, new this(...args));
        }
        
        return Singleton.__instances.get(className);
    }
}


export class CrudApi<CLS, T = object> extends Singleton<CLS> {
    prefix: string;

    protected constructor(prefix: string) {
        super();
        this.prefix = prefix;
    }

    resHandle(res: any) {
        return res.data;
    }

    // Create One
    async create(data?: T) {
        return request<any, 'json'>({
            url: `/${this.prefix}/create`,
            method: 'post',
            data
        });
    }

    // Delete By Key
    async delete(key?: number) {
        let params = new URLSearchParams();
        params.append('item_id', `${key}`);
        let str_params = params.toString();
        if (str_params.length > 0) {
            str_params = '?' + str_params;
        }

        return request<any, 'json'>({
            url: `/${this.prefix}/delete/${str_params}`,
            method: 'post'
        });
    }


    // Delete All
    async delete_all(data?: T) {
        return request<any, 'json'>({
            url: `/${this.prefix}/delete_all`,
            method: 'post'
        });
    }

    // Update One By Key
    async update(data?: T) {
        return request<any, 'json'>({
            url: `/${this.prefix}/update`,
            method: 'post',
            data
        });
    }


    // Get One By Filter Value
    async get_by_id(data?: number | string) {
        return request<any, 'json'>({
            url: `/${this.prefix}/get_by_id?item_id=${data}`,
            method: 'post'
        });
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

        return request<any, 'json'>({
            url: `/${this.prefix}/get_one_by_filter${str_params}`,
            method: 'post',
            data
        });
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

        return request<any, 'json'>({
            url: `/${this.prefix}/list${str}`,
            method: 'post'
        });
    }


    // Query Many By Filter Value
    async query(data?: T, params: string | null = null) {
        if (params && params.length > 0) {
            params = '?' + params;
        }

        return request<any, 'json'>({
            url: `/${this.prefix}/query${params}`,
            method: 'post',
            data
        });
    }


    // Query Many By Filter Condition, [=, !=, >, <, >=, <=, like, in]
    async query_ex(data?: T) {
        return request<any, 'json'>({
            url: `/${this.prefix}/query_ex`,
            method: 'post',
            data
        });
    }

    // Insert Or Update
    async upsert(data?: T) {
        return request<any, 'json'>({
            url: `/${this.prefix}/upsert`,
            method: 'post',
            data
        });
    }
}


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