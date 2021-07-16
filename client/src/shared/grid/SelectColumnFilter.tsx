import React from "react";
// Default column filter for react-table. Text input search

type Props = {
  column: any;
};

const SelectColumnFilter = ({
  column: { filterValue, preFilteredRows, setFilter, id },
}: Props) => {
  // Calculate the options for filtering
  // using the preFilteredRows
  const options = React.useMemo(() => {
    const set = new Set<any>();
    preFilteredRows.forEach((row: any) => {
      set.add(row.values[id]);
    });
    const selectValues = Array.from(set);
    const orderedValues = selectValues.sort();
    return orderedValues;
  }, [id, preFilteredRows]);

  // Render a multi-select box
  return (
    <select
      className="form-control"
      value={filterValue}
      onChange={(e) => {
        setFilter(e.target.value || undefined);
      }}
    >
      <option value="">All</option>
      {options.map((option, i) => (
        <option key={i} value={option}>
          {option}
        </option>
      ))}
    </select>
  );
};

export default SelectColumnFilter;
