import { useParams } from "react-router-dom";
import BaseFrame from "../../components/Base/Frame";

function SpiderDetailsPage() {
  const { spiderName } = useParams();
  return (
    <div id="spiderDetails">
      <BaseFrame title={spiderName!} isBack>
        <div className="flex flex-col lg:flex-row gap-8">
          {/*---------- spider details section ----------*/}
          <div className="main-card w-full lg:w-2/5 px-10 py-7">
            <div className="flex justify-between items-center">
              <h3 className="text-xl font-semibold">Spider details</h3>
              <button className="btn-primary text-white bg-error py-1">
                Stop
              </button>
            </div>
            <div className="divider my-3"></div>
            <div className="spider-details-row">
              <h4>State : </h4>
              <span className="spider-details-row__status">Active</span>
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
          {/*---------- requests chart section ----------*/}
          <div className="main-card w-full lg:w-3/5 px-10 py-7"></div>
        </div>
      </BaseFrame>
    </div>
  );
}

export default SpiderDetailsPage;
