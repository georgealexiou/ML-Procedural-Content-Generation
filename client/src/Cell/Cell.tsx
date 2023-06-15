import React from 'react';
import { ColorValue, Pressable, View } from 'react-native';
import { styles } from './styles';
import { isUpperCase } from '../utils/gridUtils';

type CellProps = {
  setCurrentLetter: React.Dispatch<React.SetStateAction<string>>;
  grid: string[][];
  rowIndex: number;
  columnIndex: number;
  setIsDrawing: React.Dispatch<React.SetStateAction<boolean>>;
  colorMap: { [key: string]: ColorValue };
};

export const Cell: React.FC<CellProps> = ({
  grid,
  rowIndex,
  columnIndex,
  setCurrentLetter,
  setIsDrawing,
  colorMap,
}) => {
  const cell: string = grid[rowIndex][columnIndex];
  const onTouchStart = () => {
    if (cell !== '') {
      setCurrentLetter(cell);
      setIsDrawing(true);
      return;
    } else {
      setIsDrawing(false);
    }
  };

  return (
    <Pressable style={styles.cellPressable} onTouchStart={onTouchStart}>
      {isUpperCase(cell) ? (
        <View style={{ backgroundColor: colorMap[cell], ...styles.node }} />
      ) : (
        <View
          style={{
            backgroundColor: cell ? colorMap[cell.toUpperCase()] : 'black',
            ...styles.connection,
          }}
        />
      )}
    </Pressable>
  );
};
