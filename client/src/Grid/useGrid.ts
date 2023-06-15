import { useCallback, useState } from 'react';
import { calculateGridSize, generateColorMap, parseStringToGrid, isSameColor } from '../utils/gridUtils';

export const useGrid = ({
  gridString,
  moveCount,
  setMoveCount,
}: {
  gridString: string;
  moveCount: number;
  setMoveCount: React.Dispatch<React.SetStateAction<number>>;
}) => {
  const gridSize = calculateGridSize(gridString);
  const colorMap = generateColorMap(gridString);

  const [currentLetter, setCurrentLetter] = useState<string>('');
  const [grid, setGrid] = useState<string[][]>(parseStringToGrid(gridString, gridSize));

  const [layout, setLayout] = useState(null);
  const [isDrawing, setIsDrawing] = useState(false);

  const handleLayout = useCallback((event) => {
    setLayout(event.nativeEvent.layout);
  }, []);

  const hasSameColorAdjacent = (rowIndex: number, columnIndex: number) => {
    if (columnIndex + 1 < gridSize && isSameColor(grid[rowIndex][columnIndex + 1], currentLetter)) return true;
    if (columnIndex - 1 >= 0 && isSameColor(grid[rowIndex][columnIndex - 1], currentLetter)) return true;
    if (rowIndex + 1 < gridSize && isSameColor(grid[rowIndex + 1][columnIndex], currentLetter)) return true;
    if (rowIndex - 1 >= 0 && isSameColor(grid[rowIndex - 1][columnIndex], currentLetter)) return true;
    return false;
  };

  const handleTouchMove = useCallback(
    (event) => {
      if (!layout) return;

      const { pageX, pageY } = event.nativeEvent;
      const rowIndex = Math.floor((pageY - layout.y) / 60);
      const columnIndex = Math.floor((pageX - layout.x) / 60);

      if (isDrawing && rowIndex >= 0 && rowIndex < grid.length && columnIndex >= 0 && columnIndex < grid[0].length) {
        const newGrid = [...grid];
        if (newGrid[rowIndex][columnIndex]) return;
        if (!hasSameColorAdjacent(rowIndex, columnIndex)) return;
        newGrid[rowIndex][columnIndex] = currentLetter.toLowerCase();
        setGrid(newGrid);
        setMoveCount(moveCount + 1);
      }
    },
    [layout, isDrawing]
  );

  return {
    grid,
    colorMap,
    setCurrentLetter,
    handleLayout,
    handleTouchMove,
    setIsDrawing,
    gridSize,
    setGrid,
  };
};
