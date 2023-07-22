import BaseFrame from "../components/Base/Frame";
import SpidersTable from "../components/Dashboard/SpidersTable";

function index() {
  return (
    <div id="index">
      <BaseFrame title="Dashboard">
        <div className="flex flex-col md:flex-row gap-8 mb-8">
          <div className="card w-full md:w-1/2 py-5 px-6">
            <h3 className="text-xl font-semibold">request per second</h3>
            <div className="divider my-3"></div>
          </div>
          <div className="card w-full md:w-1/2 py-5 px-6">
            <h3 className="text-xl font-semibold">Spider running state</h3>
            <div className="divider my-3"></div>
          </div>
        </div>
        <SpidersTable />
      </BaseFrame>
    </div>
  );
}

export default index;
