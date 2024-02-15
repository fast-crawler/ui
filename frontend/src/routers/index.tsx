import Icon from "@mdi/react";
import { mdiViewGrid, mdiSpider } from "@mdi/js";

import { Router } from "../constants/types";
import IndexPage from "../pages/index";
import SpidersPage from "../pages/spiders/index";
import SpiderDetailsPage from "../pages/spiders/details";

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
  {
    path: "/spiders/:spiderName",
    name: "SpiderDetails",
    isShowSideBar: false,
    hasChild: false,
    element: <SpiderDetailsPage />,
  },
];
