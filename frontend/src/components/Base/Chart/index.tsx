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
import { IDataSet } from "../../../constants/types";

export interface BaseChartProps {
  datasets: IDataSet[];
  labels: string[];
}

function BaseChart({ datasets, labels }: BaseChartProps) {
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
  const setBackground = (context: ScriptableContext<"line">, color: string) => {
    const ctx = context.chart.ctx;
    const gradient = ctx.createLinearGradient(0, 0, 0, 250);
    gradient.addColorStop(0, color);
    gradient.addColorStop(1, "transparent");
    return gradient;
  };

  const colorWithOpacity = (hexColor: string, opacity: number) => {
    hexColor = hexColor.replace("#", "");

    const r = parseInt(hexColor.slice(0, 2), 16);
    const g = parseInt(hexColor.slice(2, 4), 16);
    const b = parseInt(hexColor.slice(4, 6), 16);

    return `rgba(${r}, ${g}, ${b}, ${opacity})`;
  };

  return (
    <>
      <Line
        className="!h-[256px] mx-auto w-full"
        options={CHART_OPTIONS}
        data={{
          labels,
          datasets: datasets.map((item) => ({
            fill: true,
            label: item.label,
            data: item.data,
            pointBackgroundColor: item.color,
            borderColor: item.color,
            backgroundColor: (context) =>
              setBackground(context, colorWithOpacity(item.color, 0.2)),
            // cubicInterpolationMode: "monotone",
          })),
        }}
      />
    </>
  );
}

export default BaseChart;
