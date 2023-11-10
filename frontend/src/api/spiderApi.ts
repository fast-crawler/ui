import request from "./base";

export function useSpiderApi() {
  const getSpiders = async (params: any = {}) => {
    return await request({
      url: "/all",
      method: "get",
      params,
    });
  };

  const toggleTask = async (data: any) => {
    return await request({
      url: "/toggle_task",
      method: "post",
      data,
    });
  };

  const toggleTasks = async (data: any, isStart: boolean = false) => {
    return await request({
      url: isStart ? "/start_tasks" : "/stop_tasks",
      method: "post",
      data,
    });
  };

  return {
    getSpiders,
    toggleTask,
    toggleTasks,
  };
}
