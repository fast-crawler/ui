import { useState } from "react";

import BaseFrame from "../components/Base/Frame";
import SpidersTable from "../components/Dashboard/SpidersTable";
import BaseChart from "../components/Base/Chart";

function index() {
  const requestsLabels = ["1", "2", "3", "4", "5", "6"];
  const [requests] = useState([20, 16, 5, 38, 30, 22]);

  const spiderLabels = ["18:00", "19:00", "20:00", "21:00", "22:00", "23:00"];
  const [spiderData] = useState([2, 4, 10, 6, 8, 2]);

  return (
    <div id="index">
      <BaseFrame title="Dashboard">
        <div className="flex flex-col md:flex-row gap-8 mb-8">
          <div className="main-card w-full md:w-1/2 py-5 px-6">
            <h3 className="text-xl font-semibold">request per second</h3>
            <div className="divider my-3"></div>
            <BaseChart data={requests} labels={requestsLabels} />
          </div>
          <div className="main-card w-full md:w-1/2 py-5 px-6">
            <h3 className="text-xl font-semibold">Spider running state</h3>
            <div className="divider my-3"></div>
            <BaseChart data={spiderData} labels={spiderLabels} />
          </div>
        </div>
        <SpidersTable />
        <div className="mb-16"></div>
      </BaseFrame>
    </div>
  );
}

export default index;
