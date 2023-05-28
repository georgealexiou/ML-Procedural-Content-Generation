import { useState } from 'react';
import { calculateGridSize, generateColorMap, parseStringToGrid } from './gridUtils';
import { ColorValue } from 'react-native';

export const useGrid = ({ gridString }: { gridString: String }) => {
  const gridSize = calculateGridSize(gridString);
  const colorMap = generateColorMap(gridString);

  const [currentColor, setCurrentColor] = useState<ColorValue>('');
  const [currentLetter, setCurrentLetter] = useState<String | null>(null);
  const [grid, setGrid] = useState<(String | null)[][]>(parseStringToGrid(gridString, gridSize));

  return {
    gridSize,
    grid,
    setGrid,
    colorMap,
    currentColor,
    setCurrentColor,
    currentLetter,
    setCurrentLetter,
  };
};
