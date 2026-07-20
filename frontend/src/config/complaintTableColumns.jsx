import StatusBadge from "../components/common/StatusBadge";
import PriorityBadge from "../components/common/PriorityBadge";

export const OFFICE_COMPLAINT_COLUMNS = [
  {
    key: "complaint_number",
    label: "Complaint No.",
  },

  {
    key: "student_name",
    label: "Student",
  },

  {
    key: "category",
    label: "Category",

    render: (value) => value.name,
  },

  {
    key: "priority",
    label: "Priority",

    render: (value) => <PriorityBadge priority={value} />,
  },

  {
    key: "status",
    label: "Status",

    render: (value, row) => <StatusBadge status={row.status === "resolved" && row.is_confirmed ? "confirmed" : row.status} />,
  },

  {
    key: "created_at_human",
    label: "Created",
  },
];
