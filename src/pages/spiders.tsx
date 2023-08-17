import { useState } from "react";
import { Icon } from "@mdi/react";
import { mdiMagnify } from "@mdi/js";

import BaseFrame from "../components/Base/Frame";
import SpidersFilter from "../components/Spiders/FIlter";

function spiders() {
  const [selectedSort, setSelectedSort] = useState<number>(1);
  const [selectedState, setSelectedState] = useState<number>(1);
  const [searchName, setSearchName] = useState<string>("");
  const handleSearchChange = (event: any) => {
    setSearchName(event.target.value);
  };

  return (
    <div id="spiders">
      <BaseFrame title="Spiders">
        <div className="flex mb-96 ml-1">
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
      </BaseFrame>
    </div>
  );
}

export default spiders;
