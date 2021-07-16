import React from "react";

// Default column filter for react-table. Text input search

type Props = {
  column: any;
};

const DefaultColumnFilter = ({
  column: { filterValue, preFilteredRows, setFilter },
}: Props) => {
  const count = preFilteredRows.length;

  return (
    <input
      className="form-control"
      value={filterValue || ""}
      onChange={(e) => {
        setFilter(e.target.value || undefined); // Set undefined to remove the filter entirely
      }}
      placeholder={`Search ${count} records...`}
    />
  );
};

export default DefaultColumnFilter;
