import React from "react";
import classNames from "classnames";

// Grid cell which renders a formatted number

type Props = {
  value: number;
  className?: string;
};

const EllipsisCell = ({ value, className }: Props) => (
  <div className={classNames("ellipsis-cell ellipsis", className)}>{value}</div>
);

export default EllipsisCell;
