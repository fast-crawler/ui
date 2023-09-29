import React from "react";
import Icon from "@mdi/react";
import { useNavigate } from "react-router-dom";
import { mdiRefresh } from "@mdi/js";

import { ISpider } from "../../constants/types";

export interface SpidersDataTableProps {
  data: ISpider[];
  loading: boolean;
}

function SpidersDataTable({ data, loading }: SpidersDataTableProps) {
  const statusColor: any = {
    success: {
      text: "success",
      back: "bg-success",
    },
    finished: {
      text: "error",
      back: "bg-error",
    },
    paused: {
      text: "warning",
      back: "bg-warning",
    },
  };

  const navigate = useNavigate();

  const handleCheckboxClick = (event: React.MouseEvent<HTMLInputElement>) => {
    event.stopPropagation();
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
                <th className="w-4/12">Name</th>
                <th className="w-2/12">Started at</th>
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
                    navigate(`/spiders/${spider.name}`, {
                      state: { data: spider },
                    })
                  }
                >
                  <td className="pl-5">
                    <input
                      type="checkbox"
                      className="h-4 w-4 accent-primary"
                      onClick={handleCheckboxClick}
                    />
                  </td>
                  <td>{index + 1}</td>
                  <td className="pe-4">{spider.name}</td>
                  <td>{spider.start_cond}</td>
                  <td>{spider.timeout}</td>
                  <td>
                    <span
                      className={`badge`}
                      style={{
                        color: `var(--color-${
                          statusColor[spider.status].text
                        })`,
                        background: `var(--color-${
                          statusColor[spider.status].back
                        })`,
                      }}
                    >
                      {spider.status}
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
