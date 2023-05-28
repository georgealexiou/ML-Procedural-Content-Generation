import { useState } from 'react';
import { calculateGridSize, generateColorMap, parseStringToGrid } from './gridUtils';
import { ColorValue } from 'react-native';

export const useGrid = ({ gridString }: { gridString: String }) => {
  const [currentColor, setCurrentColor] = useState<ColorValue>('');

  const gridSize = calculateGridSize(gridString);
  const grid = parseStringToGrid(gridString, gridSize);
  const colorMap = generateColorMap(gridString);
  return {
    gridSize,
    grid,
    colorMap,
    currentColor,
    setCurrentColor,
  };
};
