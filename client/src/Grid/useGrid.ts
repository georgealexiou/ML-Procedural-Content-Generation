import { useState } from "react";
import {
  calculateGridSize,
  generateColorMap,
  parseStringToGrid,
} from "./gridUtils";

export const useGrid = ({ gridString }: { gridString: String }) => {
  const gridSize = calculateGridSize(gridString);
  const grid = parseStringToGrid(gridString, gridSize);
  const colorMap = generateColorMap(gridString);
  return {
    gridSize,
    grid,
    colorMap,
  };
};
