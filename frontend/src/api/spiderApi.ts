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

  return {
    getSpiders,
    toggleTask,
  };
}
