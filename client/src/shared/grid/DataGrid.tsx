import React, { useCallback, useMemo } from "react";
import { useTable, useFlexLayout, useFilters, useSortBy } from "react-table";
import { FixedSizeList } from "react-window";
import AutoSizer from "react-virtualized-auto-sizer";
import scrollbarWidth from "../scrollbarWidth";
import { noop } from "lodash";
import DefaultColumnFilter from "./DefaultColumnFilter";
import SelectColumnFilter from "./SelectColumnFilter";
import classNames from "classnames";
import GridCell from "./GridCell";
import EllipsisCell from "./EllipsisCell";

export { GridCell, EllipsisCell };

type DataGridProps = {
  columns: any[];
  data: any[];
  options?: any; //TableOptions<any>
  rowHeight?: number; // Default DEFAULT_ROW_HEIGHT 35
  maxHeight?: number;
  handleRowClick?: (row: any) => void;
};

type TableProps = DataGridProps & {
  parentWidth: number;
};

const DEFAULT_ROW_HEIGHT = 35;

function Table({
  columns,
  data,
  options,
  handleRowClick,
  rowHeight,
  maxHeight = Number.MAX_VALUE,
  parentWidth,
}: TableProps) {
  // Use the state and functions returned from useTable to build your UI

  const itemSize = rowHeight || DEFAULT_ROW_HEIGHT;

  const defaultColumn = useMemo(
    () => ({
      width: 100,
      disableFilters: true,
    }),
    []
  );

  const filterTypes = useMemo(
    () => ({
      // Override the default text filter to use "startWith"
      text: (rows: any, id: any, filterValue: any) => {
        return rows.filter((row: any) => {
          const rowValue = row.values[id];
          return rowValue !== undefined
            ? String(rowValue)
                .toLowerCase()
                .startsWith(String(filterValue).toLowerCase())
            : true;
        });
      },
    }),
    []
  );

  const tableOptions = useMemo(() => {
    const defaults = {
      columns,
      data,
      defaultColumn,
      filterTypes,
    };

    return { ...defaults, ...(options || {}) };
  }, [columns, data, defaultColumn, filterTypes, options]);

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    totalColumnsWidth,
    prepareRow,
  } = useTable<any>(tableOptions, useFlexLayout, useFilters, useSortBy);

  const extendHeaderProps = useCallback((column: any) => {
    const defaultProps = column.getHeaderProps(column.getSortByToggleProps());

    const className = classNames("th", column.headerClassName);

    const headerProps = { ...defaultProps, className };

    return headerProps;
  }, []);

  const RenderRow = useCallback(
    ({ index, style }) => {
      const row = rows[index];
      prepareRow(row);
      const styleProps: any = {
        ...style,
        cursor: handleRowClick ? "pointer" : "inherit",
      };
      return (
        <div
          {...row.getRowProps({
            style: styleProps,
          })}
          className="tr"
          onClick={() => {
            handleRowClick ? handleRowClick(row.original) : noop();
          }}
        >
          {row.cells.map((cell) => {
            return (
              <div {...cell.getCellProps()} className="td">
                {cell.render("Cell")}
              </div>
            );
          })}
        </div>
      );
    },
    [prepareRow, rows, handleRowClick]
  );

  const width = Math.max(totalColumnsWidth, parentWidth);

  const headerWidth = useMemo(() => {
    // If items exceed height of window, subtract scrollbar width
    if (rows.length * itemSize > maxHeight) {
      const scrollBarSize = scrollbarWidth();
      return width - scrollBarSize;
    }
    return width;
  }, [width, itemSize, maxHeight, rows.length]);

  const height = useMemo(() => {
    return Math.min(maxHeight, rows.length * itemSize);
  }, [maxHeight, itemSize, rows]);

  // Render the UI for your table
  return (
    <div
      {...getTableProps()}
      className="data-grid-table sticky-table table table-sm table-striped table-bordered table-hover mb-0"
      style={{ width: `${headerWidth}px` }}
    >
      <div className="thead" style={{ position: "relative" }}>
        {headerGroups.map((headerGroup) => (
          <div
            {...headerGroup.getHeaderGroupProps({
              style: { width: `${headerWidth}px`, display: "flex" },
            })}
            className="tr"
          >
            {headerGroup.headers.map((column) => (
              <div {...extendHeaderProps(column)}>
                {column.render("Header")}
                <span>
                  {column.isSorted ? (
                    <span>
                      {" "}
                      <i
                        className={classNames({
                          "fas fa-chevron-down": column.isSortedDesc,
                          "fas fa-chevron-up": !column.isSortedDesc,
                        })}
                      />
                    </span>
                  ) : (
                    ""
                  )}
                </span>
                {/* Render the columns filter UI */}
                <div>{column.canFilter ? column.render("Filter") : null}</div>
              </div>
            ))}
          </div>
        ))}
      </div>

      <div {...getTableBodyProps()} className="tbody fixed-size-list-outer">
        <FixedSizeList
          itemCount={rows.length}
          itemSize={itemSize}
          width={width}
          height={height}
        >
          {RenderRow}
        </FixedSizeList>
      </div>
    </div>
  );
}

const DataGrid = ({
  columns,
  data,
  options,
  rowHeight,
  maxHeight,
  handleRowClick,
}: DataGridProps) => {
  return (
    <div className="data-grid table-responsive">
      <AutoSizer disableHeight>
        {({ width }) => (
          <div
            style={{
              width: `${width}px`,
            }}
          >
            <Table
              columns={columns}
              data={data}
              options={options}
              handleRowClick={handleRowClick}
              rowHeight={rowHeight}
              maxHeight={maxHeight}
              parentWidth={width - 1}
            />
          </div>
        )}
      </AutoSizer>
    </div>
  );
};

export default DataGrid;
export { DefaultColumnFilter, SelectColumnFilter };
