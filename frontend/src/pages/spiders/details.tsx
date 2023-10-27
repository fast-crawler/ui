import { useEffect, useState } from "react";
import { useLocation, useParams } from "react-router-dom";
import Icon from "@mdi/react";
import { mdiInformationOutline } from "@mdi/js";

import { useSpiderApi } from "../../api";
import BaseFrame from "../../components/Base/Frame";
import BaseChart from "../../components/Base/Chart";
import BaseModal from "../../components/Base/Modal";

let chatSocket: WebSocket = new WebSocket("ws://127.0.0.1:8001/ws");

function SpiderDetailsPage() {
  const { spiderName } = useParams();
  const { toggleTask } = useSpiderApi();

  const [confirmDialog, setConfirmDialog] = useState<boolean>(false);

  const [requests, setRequest] = useState({
    labels: ["", "", "", "", "", ""],
    data: [0, 0, 0, 0, 0, 0],
    data1: [0, 0, 0, 0, 0, 0],
    data2: [0, 0, 0, 0, 0, 0],
  });

  const [logs, setLogs] = useState([
    {
      id: 1,
      date: "2023/08/06 - 15:45:27",
      text: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.",
    },
    {
      id: 2,
      date: "2023/08/06 - 15:45:27",
      text: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.",
    },
    {
      id: 3,
      date: "2023/08/06 - 15:45:27",
      text: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.",
    },
  ]);

  const { state } = useLocation();

  useEffect(() => {
    fetchChartData();
  }, []);

  const fetchChartData = () => {
    fetch("http://127.0.0.1:8001/{crawler_uuid}/chart?crawler_id=1")
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
              let time = resData.data.time.split("T")[1];
              let second = Math.floor(+time.split(":")[2]);
              time =
                time.split(":")[0] + ":" + time.split(":")[1] + ":" + second;
              console.log(time);
              //@ts-ignore
              setRequest((prevData) => {
                const newData = [...prevData.data, resData.data.all_requests];
                const newData1 = [
                  ...prevData.data1,
                  resData.data.successful_requests,
                ];
                const newData2 = [
                  ...prevData.data2,
                  resData.data.failed_requests,
                ];
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

  const toggleSpiderStatus = async () => {
    await toggleTask({ name: spiderName }).then((res) => {
      setConfirmDialog(false);
      state.data.disabled = !state.data.disabled;
    });
    document.getElementById("confirm-button")!.onclick = function (e) {
      const message = state.data.disabled ? "spider started" : "spider stopped";
      chatSocket?.send(
        JSON.stringify({
          content: message,
          sender: navigator.userAgent,
        })
      );
    };
  };

  return (
    <div id="spiderDetails">
      <BaseFrame title={spiderName!} isBack>
        <div className="flex flex-col xl:flex-row gap-8 w-full mb-8">
          {/*---------- spider details section ----------*/}
          <div className="main-card w-full xl:w-2/5 px-10 py-7">
            <div className="flex justify-between items-center">
              <h3 className="text-xl font-semibold">Spider details</h3>
              {state.data.disabled ? (
                <button
                  className="btn-primary text-white bg-success py-1"
                  onClick={() => setConfirmDialog(true)}
                >
                  Start
                </button>
              ) : (
                <button
                  className="btn-primary text-white bg-error py-1"
                  onClick={() => setConfirmDialog(true)}
                >
                  Stop
                </button>
              )}
            </div>
            <div className="divider my-3"></div>
            <div className="flex flex-col xl:justify-around h-4/5">
              <div className="spider-details-row">
                <h4>State : </h4>
                <span className="spider-details-row__status">
                  {state.data.status}
                </span>
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
            <BaseChart
              datasets={[
                { color: "#1b59f8", label: "total", data: requests.data },
                { color: "#b91c1c", label: "failed", data: requests.data1 },
                { color: "#059669", label: "success", data: requests.data2 },
              ]}
              labels={requests.labels}
            />
          </div>
        </div>
        {/*---------- spider logs section ----------*/}
        <div className="main-card w-full px-10 py-7 mb-10">
          <h3 className="text-xl font-semibold">request per second</h3>
          <div className="divider my-3"></div>
          {logs.map((log, index) => (
            <div
              key={log.id}
              className="spider-logs-row flex-wrap lg:flex-nowrap"
            >
              <h4 className="mr-5">{index + 1}</h4>
              <h4 className="mr-16">{log.date}</h4>
              <h5>{log.text}</h5>
            </div>
          ))}
        </div>
      </BaseFrame>
      <BaseModal isOpen={confirmDialog} setIsOpen={setConfirmDialog}>
        <div className="flex flex-col items-center gap-4">
          <Icon
            color={"var(--color-primary)"}
            path={mdiInformationOutline}
            size={2}
          />
          <h3 className="text-xl font-semibold">Are you sure !</h3>
          <h4 className="text-text text-center font-medium">
            by performing this action spider will be started/stopped
          </h4>
          <div className="flex w-full gap-4">
            <button
              className="btn-primary w-1/2"
              onClick={() => setConfirmDialog(false)}
            >
              Cancel
            </button>
            <button
              id="confirm-button"
              className="btn-primary w-1/2 text-white bg-primary"
              onClick={toggleSpiderStatus}
            >
              Confirm
            </button>
          </div>
        </div>
      </BaseModal>
    </div>
  );
}

export default SpiderDetailsPage;
