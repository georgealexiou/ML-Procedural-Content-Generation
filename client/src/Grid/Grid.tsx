import { View } from 'react-native';
import { useGrid } from './useGrid';
import { Cell } from '../Cell/Cell';
import React from 'react';
import { styles } from './styles';

type GridProps = {
  gridString: string;
};
export const Grid: React.FC<GridProps> = ({ gridString }) => {
  const { grid, colorMap, setCurrentLetter, handleLayout, handleTouchMove, setIsDrawing } = useGrid({
    gridString,
  });

  return (
    <View
      onLayout={handleLayout}
      onTouchEnd={() => setIsDrawing(null)}
      onTouchMove={handleTouchMove}
      style={styles.grid}>
      {grid.map((row, rowIndex) => (
        <View key={rowIndex} style={styles.row}>
          {row.map((cell, cellIndex) => (
            <Cell
              setCurrentLetter={setCurrentLetter}
              grid={grid}
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
