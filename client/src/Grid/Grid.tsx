import { View } from 'react-native';
import { useGrid } from './useGrid';
import { Cell } from '../Cell/Cell';
import React from 'react';

type GridProps = {
  gridString: string;
};
export const Grid: React.FC<GridProps> = ({ gridString }) => {
  const {
    grid,
    setGrid,
    colorMap,
    currentColor,
    setCurrentColor,
    currentLetter,
    setCurrentLetter,
    gridSize,
    handleLayout,
    handleTouchMove,
    setIsDrawing,
  } = useGrid({
    gridString,
  });

  return (
    <View
      onLayout={handleLayout}
      onTouchEnd={() => setIsDrawing(null)}
      onTouchMove={handleTouchMove}
      style={{
        flexDirection: 'column',
        borderTopWidth: 10,
        borderLeftWidth: 10,
        borderColor: 'black',
      }}>
      {grid.map((row, rowIndex) => (
        <View key={rowIndex} style={{ flexDirection: 'row' }}>
          {row.map((cell, cellIndex) => (
            <Cell
              color={colorMap[cell]}
              currentColor={currentColor}
              currentLetter={currentLetter}
              setCurrentLetter={setCurrentLetter}
              setCurrentColor={setCurrentColor}
              grid={grid}
              setGrid={setGrid}
              rowIndex={rowIndex}
              columnIndex={cellIndex}
              setIsDrawing={setIsDrawing}
              colorMap={colorMap}
            />
          ))}
        </View>
      ))}
    </View>
  );
};
