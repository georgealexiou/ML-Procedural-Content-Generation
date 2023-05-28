import React from 'react';
import { useState } from 'react';
import { ColorValue, Pressable, View } from 'react-native';

type CellProps = {
  color: ColorValue;
  currentColor: ColorValue;
  setCurrentColor: React.Dispatch<React.SetStateAction<ColorValue>>;
  currentLetter: String | null;
  setCurrentLetter: React.Dispatch<React.SetStateAction<String | null>>;
  grid: (String | null)[][];
  setGrid: React.Dispatch<React.SetStateAction<(String | null)[][]>>;
  rowIndex: number;
  columnIndex: number;
};

export const Cell: React.FC<CellProps> = ({
  color,
  currentColor,
  setCurrentColor,
  grid,
  setGrid,
  rowIndex,
  columnIndex,
  currentLetter,
  setCurrentLetter,
}) => {
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
        if (color) {
          setCurrentColor(color);
          setCurrentLetter(grid[rowIndex][columnIndex]);
          return;
        }
      }}
      onTouchMove={() => {
        if (color) return;
        if (currentColor && currentLetter) {
          setHighlightedColor(currentColor);
          const newGrid = grid;
          newGrid[rowIndex][columnIndex] = currentLetter.toLowerCase();
        }

        console.log(grid);
      }}>
      {highlightedColor ? (
        <View
          style={{
            backgroundColor: highlightedColor,
            height: '100%',
            aspectRatio: 1,
            opacity: 0.3,
          }}
        />
      ) : (
        <View
          style={{
            backgroundColor: color,
            height: '100%',
            aspectRatio: 1,
          }}
        />
      )}
    </Pressable>
  );
};
