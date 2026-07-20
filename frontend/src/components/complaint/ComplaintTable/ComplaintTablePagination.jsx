import { FiChevronLeft, FiChevronRight } from "react-icons/fi";

import "./ComplaintTablePagination.css";

import { PAGE_SIZE } from "../../../constants/pagination";

function ComplaintTablePagination({ pagination, onPageChange }) {
  // if (!pagination || pagination.count === 0 || pagination.totalPages <= 1) {
  //   return null;
  // }

  if (!pagination) return null;

  const start = (pagination.currentPage - 1) * PAGE_SIZE + 1;

  const end = Math.min(pagination.currentPage * PAGE_SIZE, pagination.count);

  return (
    <div className="complaint-pagination">
      <button
        type="button"
        className="pagination-button"
        disabled={!pagination.previous}
        onClick={() => onPageChange(pagination.currentPage - 1)}
      >
        <FiChevronLeft />
        Previous
      </button>

      <div className="pagination-info">
        Showing <strong>{start}</strong>–<strong>{end}</strong> of{" "}
        <strong>{pagination.count}</strong> complaints
      </div>

      <button
        type="button"
        className="pagination-button"
        disabled={!pagination.next}
        onClick={() => onPageChange(pagination.currentPage + 1)}
      >
        Next
        <FiChevronRight />
      </button>
    </div>
  );
}

export default ComplaintTablePagination;
