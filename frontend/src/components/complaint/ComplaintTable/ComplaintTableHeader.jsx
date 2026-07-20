function ComplaintTableHeader({ columns }) {
  return (
    <thead>
      <tr>
        {columns.map((column) => (
          <th key={column.key}>{column.label}</th>
        ))}

        <th className="actions-column">Actions</th>
      </tr>
    </thead>
  );
}

export default ComplaintTableHeader;
