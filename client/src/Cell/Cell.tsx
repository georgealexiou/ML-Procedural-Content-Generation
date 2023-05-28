import React from 'react';
import { useState } from 'react';
import { ColorValue, Pressable, View } from 'react-native';

type CellProps = {
  color: ColorValue;
  currentColor: ColorValue;
  setCurrentColor: React.Dispatch<React.SetStateAction<ColorValue>>;
  currentLetter: string;
  setCurrentLetter: React.Dispatch<React.SetStateAction<string>>;
  grid: string[][];
  setGrid: React.Dispatch<React.SetStateAction<string[][]>>;
  rowIndex: number;
  columnIndex: number;
  setIsDrawing: React.Dispatch<React.SetStateAction<boolean>>;
  colorMap: {
    [key: string]: ColorValue;
  };
};

export const Cell: React.FC<CellProps> = ({
  color,
  setCurrentColor,
  grid,
  rowIndex,
  columnIndex,
  setCurrentLetter,
  setIsDrawing,
  colorMap,
  currentColor,
}) => {
  const cell: string = grid[rowIndex][columnIndex];
  return (
    <Pressable
      style={{
        width: 60,
        height: 60,
        justifyContent: 'center',
        alignItems: 'center',
        borderRightWidth: 10,
        borderBottomWidth: 10,
      }}
      onTouchStart={() => {
        if (cell !== '') {
          setCurrentColor(color);
          setCurrentLetter(cell);
          setIsDrawing(true);
          return;
        } else {
          setIsDrawing(false);
        }
      }}>
      {isUpperCase(cell) ? (
        <View
          style={{
            backgroundColor: colorMap[cell],
            height: '100%',
            aspectRatio: 1,
          }}
        />
      ) : (
        <View
          style={{
            backgroundColor: cell ? colorMap[cell.toUpperCase()] : 'black',
            height: '100%',
            aspectRatio: 1,
            opacity: 0.3,
          }}
        />
      )}
    </Pressable>
  );
};

function isUpperCase(str) {
  if (!str) return false;
  return str === str.toUpperCase() && /[A-Z]/.test(str);
}
