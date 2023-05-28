import { View } from 'react-native';
import { useGrid } from './useGrid';
import { Cell } from '../Cell/Cell';
import React, { useState } from 'react';

type GridProps = {
  gridString: String;
};
export const Grid: React.FC<GridProps> = ({ gridString }) => {
  const { grid, setGrid, colorMap, currentColor, setCurrentColor, currentLetter, setCurrentLetter } = useGrid({
    gridString,
  });

  const [highlightedColor, setHighlightedColor] = useState<ColorValue | undefined>();

  return (
    <View
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
            />
          ))}
        </View>
      ))}
    </View>
  );
};
