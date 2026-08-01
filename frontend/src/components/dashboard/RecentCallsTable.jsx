import { Link } from "react-router-dom";
import Table from "../common/Table";
import Badge from "../common/Badge";
import { getStatusColor, getScoreColor, formatDate } from "../../utils/helpers";

// Shows a list of calls in a table.
// Clicking a row goes to the call details page.
function RecentCallsTable({ calls }) {
  const columns = [
    { header: "Customer", accessor: "customerName" },
    { header: "Advisor", accessor: "advisorName" },
    { header: "Date", accessor: "date" },
    { header: "Score", accessor: "score" },
    { header: "Status", accessor: "status" },
    { header: "", accessor: "action" },
  ];

  return (
    <Table
      columns={columns}
      data={calls}
      renderCell={(row, col) => {
        if (col.accessor === "date") return formatDate(row.date);

        if (col.accessor === "score")
          return <span className={`font-semibold ${getScoreColor(row.score)}`}>{row.score}</span>;

        if (col.accessor === "status")
          return <Badge colorClass={getStatusColor(row.status)}>{row.status}</Badge>;

        if (col.accessor === "action")
          return (
            <Link
              to={`/calls/${row.id}`}
              className="text-[var(--color-primary)] text-sm font-medium hover:underline"
            >
              View
            </Link>
          );

        return row[col.accessor];
      }}
    />
  );
}

export default RecentCallsTable;
