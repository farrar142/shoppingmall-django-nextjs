import { Box, colors } from "@mui/material";
import { CSSProperties, Dispatch, ReactNode, useState } from "react";
interface PieRenderProps {
  children?: ReactNode;
  style?: CSSProperties;
  mainColor?: string;
  subColor?: string;
  itemWidth?: number;
  max?: number;
  value: number;
  outerHeight?: number;
  itemHeight?: number;
  onChange: any;
}
const PieRender = (props: PieRenderProps) => {
  const {
    children,
    max,
    value,
    onChange,
    mainColor,
    subColor,
    outerHeight,
    itemHeight,
    itemWidth,
  } = props;
  function range(_maxNum: number, size: number): Array<number> {
    let array = [];
    for (let i = size; i <= _maxNum; i = i + size) {
      array.push(i);
    }
    return array;
  }
  const main = mainColor ? mainColor : colors.purple[900];
  const sub = subColor ? subColor : colors.purple[200];
  const _outerHeight = outerHeight ? outerHeight : 150;
  const _innerHeight = itemHeight ? itemHeight : 20;
  const _itemWidth = itemWidth ? itemWidth : 3.5;
  const _max = max ? max : 100;
  const currentOffset = (value * 100) / _max; //200*100/100 = 200 idx=200
  const size = 2;
  const count = range(100, size);
  const degree = 360 / count.length;
  const onMouseHandler = (e: any, val: number): void => {
    if (onChange) {
      onChange(e, (val * _max) / 100);
    }
  };
  return (
    <div
      style={{
        width: `${_outerHeight}px`,
        height: `${_outerHeight}px`,
      }}
    >
      <div
        style={{
          position: "relative",
          ...props.style,
        }}
      >
        {count.map((res, index) => (
          <div
            key={res}
            style={{
              position: "absolute",
              width: `${_itemWidth}px`,
              height: `${_outerHeight / 2}px`,
              // borderRadius: "50%",
              bottom: `${-_outerHeight / 2}px`,
              left: `${_outerHeight / 2 - _itemWidth / 2}px`,
              transformOrigin: "bottom center",
              transform: `rotate(${(index + 1) * degree}deg)`,
              zIndex: 10,
            }}
            onMouseOver={(e) => onMouseHandler(e, res)}
          >
            <div
              style={{
                height: `${_innerHeight}px`,
                width: `${_itemWidth}px`,
                backgroundColor: `${currentOffset >= res ? main : sub}`,
                transform: `perspective(${_innerHeight}px) rotateX(-25deg)`,
              }}
            ></div>
          </div>
        ))}
        <div
          style={{
            width: `${_outerHeight}px`,
            height: `${_outerHeight}px`,
            position: "absolute",
            zIndex: 5,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            // transform: `translate(${_outerHeight / 2}px, ${_outerHeight / 2}px)`,
          }}
        >
          <div>
            {children}
            <div>
              {value}/{_max}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
export default PieRender;
