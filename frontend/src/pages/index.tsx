import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import BaseFrame from "../components/Base/Frame";
import BaseChart from "../components/Base/Chart";
import { IOverviewData } from "../constants/types";

function index() {
  const [requests, setRequests] = useState({
    labels: ["", "", "", "", "", ""],
    data: [0, 0, 0, 0, 0, 0],
    data1: [0, 0, 0, 0, 0, 0],
    data2: [0, 0, 0, 0, 0, 0],
  });

  const [overviewData, setOverviewData] = useState<IOverviewData>({
    currentTime: "",
    allCrawlers: 0,
    activeCrawlers: 0,
    deactiveCrawlers: 0,
    totalRequests: 0,
    successfullRequests: 0,
    failedRequests: 0,
  });

  const navigate = useNavigate();

  useEffect(() => {
    const abortController = new AbortController();
    const signal = abortController.signal;

    const fetchOverviewData = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8001/dashboard/crawlers",
          { signal }
        );
        const reader = response.body!.getReader();
        while (true) {
          const { done, value } = await reader.read();
          if (done) {
            console.log("Stream finished");
            break;
          }
          const chunkString = new TextDecoder().decode(value);
          const resData = JSON.parse(chunkString);
          const time = new Date(resData.data.time).toLocaleString();
          setOverviewData((prevData) => ({
            ...prevData,
            currentTime: time,
            allCrawlers: resData.data.all_crawlers,
            activeCrawlers: resData.data.active_crawlers,
            deactiveCrawlers: resData.data.deactive_crawlers,
          }));
        }
      } catch (error) {
        console.warn("Warning in fetching overview data:", error);
      }
    };

    const fetchChartData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8001/dashboard/chart", {
          signal,
        });
        const reader = response.body!.getReader();
        while (true) {
          const { done, value } = await reader.read();
          if (done) {
            console.log("Stream finished");
            break;
          }
          const chunkString = new TextDecoder().decode(value);
          const resData = JSON.parse(chunkString);
          let time = resData.data.time.split("T")[1];
          let second = Math.floor(+time.split(":")[2]);
          time = time.split(":")[0] + ":" + time.split(":")[1] + ":" + second;

          setRequests((prevData) => {
            const newData = [...prevData.data, resData.data.all_requests];
            const newData1 = [
              ...prevData.data1,
              resData.data.successful_requests,
            ];
            const newData2 = [...prevData.data2, resData.data.failed_requests];
            const newLabels = [...prevData.labels, time];
            newData.splice(0, 1);
            newData1.splice(0, 1);
            newData2.splice(0, 1);
            newLabels.splice(0, 1);
            return {
              data: newData,
              data1: newData1,
              data2: newData2,
              labels: newLabels,
            };
          });

          setOverviewData((prevData) => ({
            ...prevData,
            totalRequests: resData.data.all_requests,
            successfulRequests: resData.data.successful_requests,
            failedRequests: resData.data.failed_requests,
          }));
        }
      } catch (error) {
        console.warn("Warning in fetching chart data:", error);
      }
    };

    fetchOverviewData();
    fetchChartData();

    return () => {
      abortController.abort();
    };
  }, [navigate]);

  return (
    <div id="index">
      <BaseFrame title="Dashboard">
        <div className="flex flex-col xl:flex-row gap-8 mb-8">
          <div className="main-card w-full xl:w-2/5 py-5 px-6">
            <h3 className="text-xl font-semibold">Overview</h3>
            <div className="divider my-3"></div>
            <div className="flex flex-col xl:justify-around h-4/5">
              <div className="spider-details-row mt-2">
                <h4>current time : </h4>
                <h5>{overviewData.currentTime}</h5>
              </div>
              <div className="spider-details-row">
                <h4>all crawlers : </h4>
                <h5>{overviewData.allCrawlers}</h5>
              </div>
              <div className="spider-details-row">
                <h4>active crawlers : </h4>
                <h5>{overviewData.activeCrawlers}</h5>
              </div>
              <div className="spider-details-row">
                <h4>deactive crawlers : </h4>
                <h5>{overviewData.deactiveCrawlers}</h5>
              </div>
              <div className="spider-details-row">
                <h4>total requests :</h4>
                <h5>{overviewData.totalRequests}</h5>
              </div>
              <div className="spider-details-row">
                <h4>successfull requests : </h4>
                <h5>{overviewData.successfullRequests}</h5>
              </div>
              <div className="spider-details-row mb-0">
                <h4>failed requests : </h4>
                <h5>{overviewData.failedRequests}</h5>
              </div>
            </div>
          </div>
          <div className="main-card w-full xl:w-3/5 py-5 px-6">
            <h3 className="text-xl font-semibold">request per second</h3>
            <div className="divider my-3"></div>
            <BaseChart
              datasets={[
                { color: "#1b59f8", label: "total", data: requests.data },
                { color: "#b91c1c", label: "failed", data: requests.data1 },
                {
                  color: "#059669",
                  label: "successfull",
                  data: requests.data2,
                },
              ]}
              labels={requests.labels}
            />
          </div>
        </div>
        <div className="mb-16"></div>
      </BaseFrame>
    </div>
  );
}

export default index;
