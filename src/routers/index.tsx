import { Router } from "../constants/types";
import IndexPage from "../pages/index";
import SpidersPage from "../pages/spiders";

export const routers: Router[] = [
  {
    path: "/",
    name: "dashboard",
    iconName: "home",
    isShowSideBar: true,
    hasChild: false,
    element: <IndexPage />,
  },
  {
    path: "/spiders",
    name: "spiders",
    iconName: "spider",
    isShowSideBar: true,
    hasChild: false,
    element: <SpidersPage />,
  },
];
