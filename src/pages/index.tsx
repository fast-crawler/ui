import { useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Filler,
  Legend,
  ScriptableContext,
} from "chart.js";

import { CHART_OPTIONS } from "../constants";
import BaseFrame from "../components/Base/Frame";
import SpidersTable from "../components/Dashboard/SpidersTable";

function index() {
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Filler,
    Legend
  );

  const requestsLabels = ["1", "2", "3", "4", "5", "6"];
  const [requests, setRequests] = useState([20, 16, 5, 38, 30, 22]);

  const spiderLabels = ["18:00", "19:00", "20:00", "21:00", "22:00", "23:00"];
  const [spiderData, setSpiderData] = useState([2, 4, 10, 6, 8, 2]);

  const setBackground = (context: ScriptableContext<"line">) => {
    const ctx = context.chart.ctx;
    const gradient = ctx.createLinearGradient(0, 0, 0, 250);
    gradient.addColorStop(0, "rgba(27, 89, 248, 0.2)");
    gradient.addColorStop(1, "transparent");
    return gradient;
  };

  return (
    <div id="index">
      <BaseFrame title="Dashboard">
        <div className="flex flex-col md:flex-row gap-8 mb-8">
          <div className="main-card w-full md:w-1/2 py-5 px-6">
            <h3 className="text-xl font-semibold">request per second</h3>
            <div className="divider my-3"></div>
            <Line
              options={CHART_OPTIONS}
              data={{
                labels: requestsLabels,
                datasets: [
                  {
                    fill: true,
                    label: "requests",
                    data: requests,
                    pointBackgroundColor: "#1b59f8",
                    borderColor: "#1b59f8",
                    backgroundColor: setBackground,
                    // cubicInterpolationMode: "monotone",
                  },
                ],
              }}
            />
          </div>
          <div className="main-card w-full md:w-1/2 py-5 px-6">
            <h3 className="text-xl font-semibold">Spider running state</h3>
            <div className="divider my-3"></div>
            <Line
              options={CHART_OPTIONS}
              data={{
                labels: spiderLabels,
                datasets: [
                  {
                    fill: true,
                    label: "spider",
                    data: spiderData,
                    pointBackgroundColor: "#1b59f8",
                    borderColor: "#1b59f8",
                    backgroundColor: setBackground,
                    // cubicInterpolationMode: "monotone",
                  },
                ],
              }}
            />
          </div>
        </div>
        <SpidersTable />
        <div className="mb-16"></div>
      </BaseFrame>
    </div>
  );
}

export default index;
