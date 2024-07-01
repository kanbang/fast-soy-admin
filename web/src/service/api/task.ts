/*
 * @Descripttion: 
 * @version: 0.x
 * @Author: zhai
 * @Date: 2024-06-29 15:32:23
 * @LastEditors: zhai
 * @LastEditTime: 2024-07-01 21:33:17
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


export function fetchAddTask(data: any) {
  return request<Api.SystemManage.UserList>({
    url: '/task',
    method: 'post',
    data
  });
}


export function fetchUpdateTask(data: any) {
  return request<Api.SystemManage.UserList>({
    url: `/task/${data?.id}`,
    method: 'put',
    data
  });
}
