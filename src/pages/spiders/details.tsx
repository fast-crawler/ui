import { useParams } from "react-router-dom";
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

import { CHART_OPTIONS } from "../../constants";
import BaseFrame from "../../components/Base/Frame";
import { useState } from "react";

function SpiderDetailsPage() {
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

  const { spiderName } = useParams();

  const requestsLabels = ["1", "2", "3", "4", "5", "6"];
  const [requests] = useState([20, 16, 5, 38, 30, 22]);

  const setBackground = (context: ScriptableContext<"line">) => {
    const ctx = context.chart.ctx;
    const gradient = ctx.createLinearGradient(0, 0, 0, 250);
    gradient.addColorStop(0, "rgba(27, 89, 248, 0.2)");
    gradient.addColorStop(1, "transparent");
    return gradient;
  };
  return (
    <div id="spiderDetails">
      <BaseFrame title={spiderName!} isBack>
        <div className="flex flex-col xl:flex-row gap-8 w-full">
          {/*---------- spider details section ----------*/}
          <div className="main-card w-full xl:w-2/5 px-10 py-7">
            <div className="flex justify-between items-center">
              <h3 className="text-xl font-semibold">Spider details</h3>
              <button className="btn-primary text-white bg-error py-1">
                Stop
              </button>
            </div>
            <div className="divider my-3"></div>
            <div className="flex flex-col xl:justify-around h-4/5">
              <div className="spider-details-row">
                <h4>State : </h4>
                <span className="spider-details-row__status">Active</span>
              </div>
              <div className="spider-details-row">
                <h4>Started at : </h4>
                <h5>2023/08/06 - 15:45:27</h5>
              </div>
              <div className="spider-details-row">
                <h4>Duration : </h4>
                <h5>16 h 32 m</h5>
              </div>
              <div className="spider-details-row">
                <h4>Successfull requests : </h4>
                <h5>235,365</h5>
              </div>
              <div className="spider-details-row">
                <h4>Failed requests : </h4>
                <h5>21,000</h5>
              </div>
              <div className="spider-details-row mb-0">
                <h4>Total requests :</h4>
                <h5>256,365</h5>
              </div>
            </div>
          </div>
          {/*---------- requests chart section ----------*/}
          <div className="main-card w-full xl:w-3/5 px-10 py-7">
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
        </div>
      </BaseFrame>
    </div>
  );
}

export default SpiderDetailsPage;
