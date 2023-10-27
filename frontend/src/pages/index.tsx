import { useEffect, useState } from "react";

import BaseFrame from "../components/Base/Frame";
import BaseChart from "../components/Base/Chart";
import { IOverviewData } from "../constants/types";

function index() {
  const requestsLabels = ["1", "2", "3", "4", "5", "6"];
  const [requests] = useState([20, 16, 5, 38, 30, 22]);

  const [overviewData, setOverviewData] = useState<IOverviewData>({
    currentTime: "",
    allCrawlers: 0,
    activeCrawlers: 0,
    deactiveCrawlers: 0,
    totalRequests: 0,
    successfullRequests: 0,
    failedRequests: 0,
  });

  useEffect(() => {
    fetchOverviewData();
  }, []);

  const fetchOverviewData = () => {
    fetch("http://127.0.0.1:8001/dashboard/crawlers")
      .then((response) => {
        const stream = response.body;
        const reader = stream!.getReader();
        const readChunk = () => {
          reader
            .read()
            .then(({ value, done }) => {
              if (done) {
                console.log("Stream finished");
                return;
              }
              const chunkString = new TextDecoder().decode(value);
              const resData = JSON.parse(chunkString);
              let time = new Date(resData.data.time).toLocaleString();
              setOverviewData((prevData) => ({
                ...prevData,
                currentTime: time,
                allCrawlers: resData.data.all_crawlers,
                activeCrawlers: resData.data.active_crawlers,
                deactiveCrawlers: resData.data.deactive_crawlers,
              }));
              readChunk();
            })
            .catch((error) => {
              console.error(error);
            });
        };
        readChunk();
      })
      .catch((error) => {
        console.error(error);
      });
  };

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
