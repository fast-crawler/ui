import React from "react";
import { useNavigate } from "react-router-dom";

function SpidersDataTable() {
  const spiders = [
    {
      id: 1,
      name: "Digikala",
      started_at: "2023/08/06 - 15:45:27",
      duration: "16 h 32 m",
      status: "Active",
    },
    {
      id: 2,
      name: "Amazon",
      started_at: "2023/08/05 - 10:20:15",
      duration: "12 h 15 m",
      status: "Paused",
    },
    {
      id: 3,
      name: "Ebay",
      started_at: "2023/08/04 - 18:30:10",
      duration: "8 h 45 m",
      status: "Finished",
    },
    {
      id: 4,
      name: "Walmart",
      started_at: "2023/08/03 - 09:12:08",
      duration: "20 h 10 m",
      status: "Active",
    },
    {
      id: 5,
      name: "Target",
      started_at: "2023/08/02 - 14:38:55",
      duration: "15 h 20 m",
      status: "Paused",
    },
    {
      id: 6,
      name: "Best Buy",
      started_at: "2023/08/01 - 20:55:40",
      duration: "10 h 5 m",
      status: "Finished",
    },
    {
      id: 7,
      name: "Alibaba",
      started_at: "2023/07/31 - 07:30:22",
      duration: "18 h 40 m",
      status: "Active",
    },
    {
      id: 8,
      name: "Newegg",
      started_at: "2023/07/30 - 12:08:17",
      duration: "22 h 15 m",
      status: "Paused",
    },
    {
      id: 9,
      name: "Newegg",
      started_at: "2023/07/30 - 12:08:17",
      duration: "22 h 15 m",
      status: "Paused",
    },
  ];

  const statusColor: any = {
    Active: {
      text: "success",
      back: "bg-success",
    },
    Finished: {
      text: "error",
      back: "bg-error",
    },
    Paused: {
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
      <table className="w-full">
        <thead className="sticky top-0 bg-white">
          <tr>
            <th className="w-1/12 pl-5">
              <input type="checkbox" className="h-4 w-4 accent-primary" />
            </th>
            <th className="w-1/12">#</th>
            <th className="w-2/12">Name</th>
            <th className="w-4/12">Started at</th>
            <th className="w-2/12">Duration</th>
            <th className="w-2/12">State</th>
          </tr>
        </thead>
        <tbody>
          {spiders.map((spider, index) => (
            <tr
              key={spider.id}
              className="hover:bg-bg-primary"
              onClick={() => navigate(`/spiders/${spider.name}`)}
            >
              <td className="pl-5">
                <input
                  type="checkbox"
                  className="h-4 w-4 accent-primary"
                  onClick={handleCheckboxClick}
                />
              </td>
              <td>{index + 1}</td>
              <td>{spider.name}</td>
              <td>{spider.started_at}</td>
              <td>{spider.duration}</td>
              <td>
                <span
                  className={`badge`}
                  style={{
                    color: `var(--color-${statusColor[spider.status].text})`,
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
    </div>
  );
}

export default SpidersDataTable;
