import { useEffect, useState } from "react";
import { Icon } from "@mdi/react";
import { mdiMagnify } from "@mdi/js";

import { useSpiderApi } from "../../api";
import { ISpiderData } from "../../constants/types";
import BaseFrame from "../../components/Base/Frame";
import SpidersFilter from "../../components/Spiders/FIlter";
import SpidersDataTable from "../../components/Spiders/DataTable";

function spiders() {
  const { getSpiders } = useSpiderApi();
  const [selectedSort, setSelectedSort] = useState<number>(1);
  const [selectedState, setSelectedState] = useState<number>(1);
  const [searchName, setSearchName] = useState<string>("");

  const handleSearchChange = (event: any) => {
    setSearchName(event.target.value);
  };

  useEffect(() => {
    fetchOverviewData();
    // getSpidersData();
  }, []);

  const [loading, setLoading] = useState<boolean>(false);
  const [spiders, setSpiders] = useState<ISpiderData[]>([]);
  const fetchOverviewData = async () => {
    try {
      await fetch("http://127.0.0.1:8001/crawler/list")
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
                try {
                  const resData = JSON.parse(chunkString);
                  // let time = new Date(resData.data.time).toLocaleString();
                  console.log(resData);
                  setSpiders(resData.data);
                } catch (error) {
                  console.log(error);
                }

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
    } catch (error) {}
  };

  const getSpidersData = async () => {
    setLoading(true);
    await getSpiders()
      .then((res) => {
        console.log(res.data);
        setSpiders([...res.data]);
      })
      .finally(() => {
        setLoading(false);
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
            <button className="btn-primary bg-error text-white">
              stop all
            </button>
            <button className="btn-primary bg-success text-white">
              start all
            </button>
          </div>
        </div>
        {/*------------ spiders data table section ------------*/}
        <SpidersDataTable data={spiders} loading={loading} />
      </BaseFrame>
    </div>
  );
}

export default spiders;
