function ComplaintTableEmpty({ colSpan, message }) {
  return (
    <tr>
      <td colSpan={colSpan} className="complaint-table-empty">
        {message}
      </td>
    </tr>
  );
}

export default ComplaintTableEmpty;
