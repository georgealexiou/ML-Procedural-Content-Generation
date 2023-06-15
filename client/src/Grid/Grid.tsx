import { Text, View } from 'react-native';
import { useGrid } from './useGrid';
import { Cell } from '../Cell/Cell';
import React, { useEffect } from 'react';
import { styles } from './styles';
import { parseStringToGrid } from '../utils/gridUtils';

type GridProps = {
  gridString: string;
  reset?: boolean;
  moveCount: number;
  setMoveCount: React.Dispatch<React.SetStateAction<number>>;
};
export const Grid: React.FC<GridProps> = ({ gridString, reset, moveCount, setMoveCount }) => {
  const { grid, colorMap, setCurrentLetter, handleLayout, handleTouchMove, setIsDrawing, gridSize, setGrid } = useGrid({
    gridString,
    moveCount,
    setMoveCount,
  });

  useEffect(() => {
    setGrid(parseStringToGrid(gridString, gridSize));
    setMoveCount(0);
  }, [reset]);

  return (
    <View
      onLayout={handleLayout}
      onTouchEnd={() => setIsDrawing(null)}
      onTouchMove={handleTouchMove}
      style={styles.grid}>
      {grid.map((row, rowIndex) => (
        <View key={rowIndex} style={styles.row}>
          {row.map((_, cellIndex) => (
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
