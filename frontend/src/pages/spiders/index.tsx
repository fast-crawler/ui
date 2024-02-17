import { useEffect, useState } from "react";
import { Icon } from "@mdi/react";
import { mdiMagnify, mdiInformationOutline } from "@mdi/js";
import { useNavigate } from "react-router-dom";

import { ISpiderData } from "../../constants/types";
import { useSpiderApi } from "../../api";
import BaseFrame from "../../components/Base/Frame";
import SpidersFilter from "../../components/Spiders/FIlter";
import SpidersDataTable from "../../components/Spiders/DataTable";
import BaseModal from "../../components/Base/Modal";

function spiders() {
  const navigate = useNavigate();

  const [selectedSort, setSelectedSort] = useState<number>(1);
  const [selectedState, setSelectedState] = useState<number>(1);
  const [searchName, setSearchName] = useState<string>("");
  const [confirmDialog, setConfirmDialog] = useState<boolean>(false);
  const [isStart, setIsStart] = useState<boolean>(false);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const { toggleTasks } = useSpiderApi();

  const handleSearchChange = (event: any) => {
    setSearchName(event.target.value);
  };

  const openConfirmDialog = (start: boolean) => {
    setIsStart(start);
    setConfirmDialog(true);
  };

  useEffect(() => {
    const abortController = new AbortController();
    const signal = abortController.signal;

    const fetchOverviewData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8001/crawler/list", {
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
          setSpiders(resData.data);
        }
      } catch (error) {
        console.warn("Warning in fetching data:", error);
      }
    };

    fetchOverviewData();

    return () => {
      abortController.abort();
    };
  }, [navigate]);

  const [loading] = useState<boolean>(false);
  const [spiders, setSpiders] = useState<ISpiderData[]>([]);

  const toggleSpidersStatus = async () => {
    await toggleTasks({ names: selectedIds }, isStart).then(() => {
      setConfirmDialog(false);
    });
  };

  return (
    <div id="spiders">
      <BaseFrame title="Spiders">
        <div className="flex justify-between mb-5">
          <div className="flex ml-1">
            {/*------------ spiders filter ------------*/}
            <SpidersFilter
              selectedSort={selectedSort}
              selectedState={selectedState}
              onSortChange={setSelectedSort}
              onStateChange={setSelectedState}
            />
            {/*------------ spider search field ------------*/}
            <div className="flex p-2 border border-border bg-white rounded-lg text-text ml-5">
              <Icon path={mdiMagnify} size={1} className="mr-2" />
              <input
                type="text"
                placeholder="Search spiders by name"
                value={searchName}
                onChange={handleSearchChange}
                className="outline-none"
              />
            </div>
          </div>
          {/*------------ action buttons ------------*/}
          <div className="flex h-10 gap-4">
            <button
              className="btn-primary bg-error text-white"
              onClick={() => openConfirmDialog(false)}
            >
              stop all
            </button>
            <button
              className="btn-primary bg-success text-white"
              onClick={() => openConfirmDialog(true)}
            >
              start all
            </button>
          </div>
        </div>
        {/*------------ spiders data table section ------------*/}
        <SpidersDataTable
          data={spiders}
          loading={loading}
          selectedIds={selectedIds}
          onSelectedIdsChange={setSelectedIds}
        />
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
            by performing this action spiders will be{" "}
            {isStart ? "started" : "stopped"}
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
              onClick={toggleSpidersStatus}
            >
              Confirm
            </button>
          </div>
        </div>
      </BaseModal>
    </div>
  );
}

export default spiders;
