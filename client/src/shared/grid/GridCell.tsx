import React from "react";
import classNames from "classnames";
import NumberFormatSpan from "../NumberFormatSpan";
import { isNil } from "lodash";

// Grid cell which renders a formatted number

type Props = {
  value: number;
  format?: string;
  className?: string;
};

const GridCell = ({
  value,
  format = "0,0",
  className = "text-center",
}: Props) => (
  <div className={classNames("result-grid-cel", className)}>
    {isNil(value) ? "-" : <NumberFormatSpan value={value} format={format} />}
  </div>
);

export default GridCell;
