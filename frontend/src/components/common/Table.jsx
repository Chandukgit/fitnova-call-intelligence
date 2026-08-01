// A simple, generic table.
// columns: [{ header: "Name", accessor: "name" }]
// data: array of objects
// renderCell (optional): (row, column) => custom JSX for a cell
function Table({ columns, data, renderCell }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm text-left">
        <thead>
          <tr className="border-b border-[var(--color-border)] text-[var(--color-text-soft)]">
            {columns.map((col) => (
              <th key={col.accessor} className="py-2 pr-4 font-medium">
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr
              key={row.id || rowIndex}
              className="border-b border-[var(--color-border)] last:border-0 hover:bg-gray-50"
            >
              {columns.map((col) => (
                <td key={col.accessor} className="py-3 pr-4 text-[var(--color-text)]">
                  {renderCell ? renderCell(row, col) : row[col.accessor]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      {data.length === 0 && (
        <p className="text-center text-[var(--color-text-soft)] py-6 text-sm">No data to show.</p>
      )}
    </div>
  );
}

export default Table;
