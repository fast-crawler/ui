import { useState } from "react";

import BaseFrame from "../components/Base/Frame";
import BaseChart from "../components/Base/Chart";

function index() {
  const requestsLabels = ["1", "2", "3", "4", "5", "6"];
  const [requests] = useState([20, 16, 5, 38, 30, 22]);

  return (
    <div id="index">
      <BaseFrame title="Dashboard">
        <div className="flex flex-col md:flex-row gap-8 mb-8">
          <div className="main-card w-full md:w-1/2 py-5 px-6">
            <h3 className="text-xl font-semibold">Spiders State</h3>
            <div className="divider my-3"></div>
            <BaseChart
              datasets={[
                { data: requests, label: "requests", color: "#1b59f8" },
              ]}
              labels={requestsLabels}
            />
          </div>
          <div className="main-card w-full md:w-1/2 py-5 px-6">
            <h3 className="text-xl font-semibold">request per second</h3>
            <div className="divider my-3"></div>
            <BaseChart
              datasets={[
                { data: requests, label: "requests", color: "#1b59f8" },
              ]}
              labels={requestsLabels}
            />
          </div>
        </div>
        <div className="mb-16"></div>
      </BaseFrame>
    </div>
  );
}

export default index;
