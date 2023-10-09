export const CHART_OPTIONS: any = {
  responsive: true,
  font: {
    family: "Inter",
  },
  interaction: {
    mode: "index",
    intersect: false,
  },
  plugins: {
    legend: {
      title: {
        font: { family: "Inter" },
        // font: { family: "Inter" },
      },
    },
    tooltip: {
      bodyFont: { family: "Inter" },
      padding: {
        x: 20,
        y: 12,
      },
    },
  },
  scales: {
    y: {
      suggestedMin: 0,
      beginAtZero: true,
      max: 100,
      ticks: {
        stepSize: 10,
      },
    },
  },
};
