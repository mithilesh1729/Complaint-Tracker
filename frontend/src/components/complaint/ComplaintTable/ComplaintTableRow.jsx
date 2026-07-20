import ComplaintTableActions from "./ComplaintTableActions";

function ComplaintTableRow({ complaint, columns, actions }) {
  return (
    <tr>
      {columns.map((column) => {
        const value = complaint[column.key];

        return (
          <td key={column.key}>
            {column.render ? column.render(value, complaint) : value}
          </td>
        );
      })}

      <td className="table-actions">
        <ComplaintTableActions complaint={complaint} actions={actions} />
      </td>
    </tr>
  );
}

export default ComplaintTableRow;
