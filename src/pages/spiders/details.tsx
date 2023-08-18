import { useParams } from "react-router-dom";
import BaseFrame from "../../components/Base/Frame";

function SpiderDetailsPage() {
  const { spiderName } = useParams();
  return (
    <div id="spiderDetails">
      <BaseFrame title={spiderName!}>
        <div>Heoolo</div>
      </BaseFrame>
    </div>
  );
}

export default SpiderDetailsPage;
