import React from "react";
import Icon from "@mdi/react";
import { useNavigate } from "react-router-dom";
import { mdiRefresh } from "@mdi/js";

import { ISpiderData } from "../../constants/types";

export interface SpidersDataTableProps {
  data: ISpiderData[];
  loading: boolean;
  selectedIds: string[];
  onSelectedIdsChange: (newValue: any) => void;
}

function SpidersDataTable({
  data,
  loading,
  onSelectedIdsChange,
}: SpidersDataTableProps) {
  const statusColor: any = {
    Active: {
      text: "success",
      back: "bg-success",
    },
    Finished: {
      text: "error",
      back: "bg-error",
    },
    Pause: {
      text: "warning",
      back: "bg-warning",
    },
  };

  const navigate = useNavigate();

  const handleCheckboxClick = (
    event: React.MouseEvent<HTMLInputElement>,
    id: string
  ) => {
    event.stopPropagation();
    onSelectedIdsChange((prevSelectedIds: any) => {
      const selectedData = [...prevSelectedIds];
      const index = selectedData.indexOf(id);
      if (index !== -1) selectedData.splice(index, 1);
      else selectedData.push(id);
      return [...selectedData];
    });
  };

  return (
    <div
      className="main-card px-4 w-full overflow-y-auto"
      style={{ height: "calc(100vh - 200px)" }}
    >
      {loading ? (
        <div className="text-center mt-10">
          <Icon
            path={mdiRefresh}
            size={1.5}
            color="var(--color-primary)"
            className="mx-auto animate-spin"
          />
        </div>
      ) : (
        data && (
          <table className="w-full">
            <thead className="sticky top-0 bg-white">
              <tr>
                <th className="w-1/12 pl-5">
                  <input type="checkbox" className="h-4 w-4 accent-primary" />
                </th>
                <th className="pe-4">#</th>
                <th className="w-3/12">Name</th>
                <th className="w-3/12">Started at</th>
                <th className="w-2/12">Duration</th>
                <th className="w-2/12">State</th>
              </tr>
            </thead>
            <tbody>
              {data.map((spider, index) => (
                <tr
                  key={spider.name}
                  className="hover:bg-bg-primary"
                  onClick={() =>
                    navigate(`/spiders/${spider.id}`, {
                      state: { data: spider },
                    })
                  }
                >
                  <td className="pl-5">
                    <input
                      type="checkbox"
                      className="h-4 w-4 accent-primary"
                      onClick={(event) =>
                        handleCheckboxClick(event, spider.name)
                      }
                    />
                  </td>
                  <td>{index + 1}</td>
                  <td className="pe-4">{spider.name}</td>
                  <td>{new Date(spider.started_at).toLocaleString()}</td>
                  <td>{spider.duration}</td>
                  <td>
                    <span
                      className={`badge`}
                      style={{
                        color: `var(--color-${statusColor[spider.state].text})`,
                        background: `var(--color-${
                          statusColor[spider.state].back
                        })`,
                      }}
                    >
                      {spider.state}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )
      )}
    </div>
  );
}

export default SpidersDataTable;
