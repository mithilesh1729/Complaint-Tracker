import "../../complaint/ComplaintTable/ComplaintTable.css";
function DataTable({
  columns,
  data,
  keyField = "id",
  loading = false,
  emptyMessage = "No records found.",
  pagination,
  onPageChange,
}) {
  if (loading) {
    return <div className="p-4 text-center">Loading...</div>; // TODO: Use Skeleton
  }

  return (
    <div className="complaint-table-container">
      <table className="complaint-table">
        <thead>
          <tr>
            {columns.map((col, index) => (
              <th key={index} style={{ width: col.width }}>
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data && data.length > 0 ? (
            data.map((row) => (
              <tr key={row[keyField]}>
                {columns.map((col, index) => (
                  <td key={index}>
                    {col.render ? col.render(row) : row[col.field]}
                  </td>
                ))}
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={columns.length} className="text-center py-5 text-muted">
                {emptyMessage}
              </td>
            </tr>
          )}
        </tbody>
      </table>

      {pagination && (
        <div className="complaint-table-pagination" style={{ padding: "16px", display: "flex", justifyContent: "space-between", borderTop: "1px solid var(--color-border)" }}>
          <button
            className="table-action-button secondary"
            disabled={!pagination.previous}
            onClick={() => onPageChange(pagination.previous)}
          >
            &larr; Previous
          </button>
          <span style={{ fontSize: "14px", color: "var(--color-text-secondary)" }}>
            Page {pagination.currentPage || 1}
          </span>
          <button
            className="table-action-button secondary"
            disabled={!pagination.next}
            onClick={() => onPageChange(pagination.next)}
          >
            Next &rarr;
          </button>
        </div>
      )}
    </div>
  );
}

export default DataTable;
