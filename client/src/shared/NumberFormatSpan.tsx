import React from "react";
import classNames from "classnames";
import numeral from "numeral";
import Skeleton from "react-loading-skeleton";

type Props = {
  value: number;
  format: string;
  isLoading?: boolean;
  loadingWidth?: number;
  className?: string;
};

const NumberFormatSpan = ({
  value,
  format,
  isLoading,
  loadingWidth,
  className,
}: Props) => {
  const isNegative = value && value < 0;
  return (
    <span className="number-format-span">
      {isLoading ? (
        <Skeleton width={loadingWidth} />
      ) : value === null ? null : (
        <span
          className={classNames(
            {
              "text-danger": isNegative,
            },
            className
          )}
        >
          {numeral(value).format(format)}
        </span>
      )}
    </span>
  );
};

export default NumberFormatSpan;
