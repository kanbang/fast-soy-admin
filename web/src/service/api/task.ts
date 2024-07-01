/*
 * @Descripttion: 
 * @version: 0.x
 * @Author: zhai
 * @Date: 2024-06-29 15:32:23
 * @LastEditors: zhai
 * @LastEditTime: 2024-06-29 15:43:20
 */
import { request } from '../request';


/** get task list */
export function fetchGetTaskList(params?: Api.SystemManage.UserSearchParams) {
    return request<Api.SystemManage.UserList>({
      url: '/task',
      method: 'get',
      params
    });
  }