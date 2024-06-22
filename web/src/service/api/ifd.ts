/*
 * @Descripttion: 
 * @version: 0.x
 * @Author: zhai
 * @Date: 2024-06-21 19:42:39
 * @LastEditors: zhai
 * @LastEditTime: 2024-06-21 20:01:57
 */
import { CrudApi } from "../crud-api";
import { FastCrudApi } from "../fast-crud-api";

import { mockRequest } from '@/service/request';

const request = mockRequest;

// export class EquipmentApi extends CrudApi<EquipmentApi> {
//     constructor() {
//         super("equipment");
//     }
// }

// export const equipment_api = EquipmentApi.instance();



export class FastEquipmentApi extends FastCrudApi<FastEquipmentApi> {
    constructor() {
        super("equipment");
    }
}

export const fast_equipment_api = FastEquipmentApi.instance();




export class FastUnitApi extends FastCrudApi<FastUnitApi> {
    constructor() {
        super("unit");
    }

    export_csv(id?: string) {
        return request({
            url: `/${this.prefix}/export_csv/${id}`,
            method: 'GET',
            responseType: "blob"
        });
    }
}

export const fast_unit_api = FastUnitApi.instance();


export class FastMfptApi extends FastCrudApi<FastMfptApi> {
    constructor() {
        super("mfpt");
    }
}

export const fast_mfpt_api = FastMfptApi.instance();

//////////////////////////////////////////////////////////////////////
export class FastMfpApi extends FastCrudApi<FastMfpApi> {
    constructor() {
        super("mfp");
    }
}

export const fast_mfp_api = FastMfpApi.instance();




export class FastMfstApi extends FastCrudApi<FastMfstApi> {
    constructor() {
        super("mfst");
    }
}

export const fast_mfst_api = FastMfstApi.instance();


//////////////////////////////////////////////////////////////////////
export class FastMfsApi extends FastCrudApi<FastMfsApi> {
    constructor() {
        super("mfs");
    }
}

export const fast_mfs_api = FastMfsApi.instance();

