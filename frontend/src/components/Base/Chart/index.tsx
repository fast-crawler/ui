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

import { CHART_OPTIONS } from "../../../constants";

export interface BaseChartProps {
  data: string[] | number[];
  labels: string[];
}

function BaseChart({ data, labels }: BaseChartProps) {
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
  const setBackground = (context: ScriptableContext<"line">) => {
    const ctx = context.chart.ctx;
    const gradient = ctx.createLinearGradient(0, 0, 0, 250);
    gradient.addColorStop(0, "rgba(27, 89, 248, 0.2)");
    gradient.addColorStop(1, "transparent");
    return gradient;
  };
  return (
    <>
      <Line
        options={CHART_OPTIONS}
        data={{
          labels,
          datasets: [
            {
              fill: true,
              label: "requests",
              data,
              pointBackgroundColor: "#1b59f8",
              borderColor: "#1b59f8",
              backgroundColor: setBackground,
              // cubicInterpolationMode: "monotone",
            },
          ],
        }}
      />
    </>
  );
}

export default BaseChart;
