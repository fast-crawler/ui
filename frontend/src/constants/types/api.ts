export interface ISpider {
  name: string;
  description: string;
  logger_name: string;
  execution: null | string;
  priority: number;
  disabled: boolean;
  force_run: boolean;
  status: string;
  timeout: null | string;
  start_cond: string | boolean;
  end_cond: string | boolean;
}

export interface ISpiderData {
  id: string;
  duration: string;
  name: string;
  started_at: string;
  state: string;
}

export interface ISpiderDetails extends ISpiderData {
  totalRequest: number;
  succesfullRequest: number;
  failedRequest: number;
}
