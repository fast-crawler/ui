import { ReactNode } from "react";

export interface Router {
  path?: string;
  name?: string;
  iconName?: string;
  isShowSideBar?: boolean;
  hasChild?: boolean;
  isOpenDropDown?: boolean;
  element?: ReactNode;
  children?: Router[];
}
