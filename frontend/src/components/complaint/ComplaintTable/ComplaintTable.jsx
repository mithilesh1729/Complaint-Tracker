import ComplaintTableHeader from "./ComplaintTableHeader";
import ComplaintTableRow from "./ComplaintTableRow";
import ComplaintTableEmpty from "./ComplaintTableEmpty";
import ComplaintTableSkeleton from "./ComplaintTableSkeleton";
import ComplaintTablePagination from "./ComplaintTablePagination";

import "./ComplaintTable.css";

function ComplaintTable({
  columns,
  data,
  actions = [],
  loading = false,
  emptyMessage = "No complaints found.",
  pagination,
  onPageChange,
}) {
  if (loading) {
    return <ComplaintTableSkeleton />;
  }

  return (
    <div className="complaint-table-container">
      <table className="complaint-table">
        <ComplaintTableHeader columns={columns} />

        <tbody>
          {data.length ? (
            data.map((complaint) => (
              <ComplaintTableRow
                key={complaint.complaint_id}
                complaint={complaint}
                columns={columns}
                actions={actions}
              />
            ))
          ) : (
            <ComplaintTableEmpty
              colSpan={columns.length + 1}
              message={emptyMessage}
            />
          )}
        </tbody>
      </table>

      {pagination && (
        <ComplaintTablePagination
          pagination={pagination}
          onPageChange={onPageChange}
        />
      )}
    </div>
  );
}

export default ComplaintTable;
