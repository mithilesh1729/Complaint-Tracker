import { PRIORITY_OPTIONS, STATUS_OPTIONS } from "./complaintOptions";

export const OFFICE_QUEUE_FILTERS = [
  {
    key: "search",
    type: "search",
    placeholder: "Search complaint number, student or category...",
  },
  {
    key: "priority",
    label: "Priority",
    type: "select",
    options: PRIORITY_OPTIONS,
  },
];

export const OFFICE_ASSIGNED_FILTERS = [
  {
    key: "search",
    type: "search",
    placeholder: "Search complaint number, student or category...",
  },
  {
    key: "priority",
    label: "Priority",
    type: "select",
    options: PRIORITY_OPTIONS,
  },
  {
    key: "status",
    label: "Status",
    type: "select",
    options: STATUS_OPTIONS,
  },
];
