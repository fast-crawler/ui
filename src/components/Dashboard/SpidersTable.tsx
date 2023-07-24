function SpidersTable() {
  return (
    <div className="main-card px-4 md:px-9 py-5 w-full overflow-x-auto">
      <div className="flex items-center justify-between mb-5">
        <h3 className="text-xl font-semibold">Last spiders</h3>
        <button className="btn-primary">See All</button>
      </div>
      <div>
        <table className="table-auto min-w-full">
          <thead>
            <tr>
              <th className="w-1/12">#</th>
              <th className="w-3/12">Name</th>
              <th className="w-4/12">Started at</th>
              <th className="w-2/12">Duration</th>
              <th className="w-2/12">State</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>Digikala</td>
              <td>2023/08/06 - 15:45:27</td>
              <td>12 h 20 m</td>
              <td>
                <span className="badge bg-bg-success text-success">Active</span>
              </td>
            </tr>
            <tr>
              <td>2</td>
              <td>DevTo</td>
              <td>2023/08/22 - 10:23:00</td>
              <td>16 h 32 m</td>
              <td>
                <span className="badge bg-bg-error text-error">Finished</span>
              </td>
            </tr>
            <tr>
              <td>3</td>
              <td>Medium</td>
              <td>2023/06/16 - 20:45:10</td>
              <td>7 h 50 m</td>
              <td>
                <span className="badge bg-bg-success text-success">Active</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default SpidersTable;
