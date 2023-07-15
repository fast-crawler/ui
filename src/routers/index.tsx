import Icon from "@mdi/react";
import { mdiViewGrid, mdiSpider } from "@mdi/js";

import { Router } from "../constants/types";
import IndexPage from "../pages/index";
import SpidersPage from "../pages/spiders";

export const routers: Router[] = [
  {
    path: "/",
    name: "Dashboard",
    icon: <Icon path={mdiViewGrid} size={1} />,
    isShowSideBar: true,
    hasChild: false,
    element: <IndexPage />,
  },
  {
    path: "/spiders",
    name: "Spiders",
    icon: <Icon path={mdiSpider} size={1} />,
    isShowSideBar: true,
    hasChild: false,
    element: <SpidersPage />,
  },
];
