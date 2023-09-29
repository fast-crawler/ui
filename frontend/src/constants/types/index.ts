import { ReactNode } from "react";

export * from "./api";

export interface Router {
  path?: string;
  name?: string;
  icon?: ReactNode;
  isShowSideBar?: boolean;
  hasChild?: boolean;
  isOpenDropDown?: boolean;
  element?: ReactNode;
  children?: Router[];
}
