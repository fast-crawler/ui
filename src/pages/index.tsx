import BaseFrame from "../components/Base/Frame";
import SpidersTable from "../components/Dashboard/SpidersTable";

function index() {
  return (
    <div id="index">
      <BaseFrame title="Dashboard">
        <SpidersTable />
      </BaseFrame>
    </div>
  );
}

export default index;
