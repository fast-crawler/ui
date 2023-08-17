import { useState } from "react";
import BaseFrame from "../components/Base/Frame";
import SpidersFilter from "../components/Spiders/FIlter";

function spiders() {
  const [selectedSort, setSelectedSort] = useState<number>(1);
  const [selectedState, setSelectedState] = useState<number>(1);

  return (
    <div id="spiders">
      <BaseFrame title="Spiders">
        <div className="flex mb-96 ml-1">
          <SpidersFilter
            selectedSort={selectedSort}
            selectedState={selectedState}
            onSortChange={setSelectedSort}
            onStateChange={setSelectedState}
          />
        </div>
      </BaseFrame>
    </div>
  );
}

export default spiders;
