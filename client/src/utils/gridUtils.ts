import { ColorValue } from 'react-native';

export const calculateGridSize = (gridString: string): number => {
  let totalCells = 0;
  [...gridString].forEach((character) => {
    totalCells += isNaN(parseInt(character)) ? 1 : parseInt(character);
  });

  return Math.floor(Math.sqrt(totalCells));
};

export const parseStringToGrid = (gridString: string, gridSize: number) => {
  const grid = [];
  let row: string[] = [];

  [...gridString].forEach((character) => {
    if (isNaN(parseInt(character))) {
      row.push(character);
    } else {
      const spaces = Array(parseInt(character)).fill('');
      row.push(...spaces);
    }

    while (row.length >= gridSize) {
      grid.push(row.slice(0, gridSize));
      row = row.slice(gridSize);
    }
  });

  if (row.length > 0) {
    grid.push(row);
  }

  return grid;
};

const predefinedColors = [
  'red',
  'green',
  'blue',
  'yellow',
  'orange',
  'purple',
  'cyan',
  'magenta',
  'lime',
  'pink',
  'teal',
  'lavender',
  'brown',
  'beige',
  'maroon',
  'navy',
];

export const generateColorMap = (gridString: string): { [key: string]: ColorValue } => {
  const uniqueLetters = [...new Set(gridString.replace(/[0-9]/g, ''))];
  const colorMap: { [key: string]: string } = {};
  uniqueLetters.forEach((letter, index) => {
    colorMap[letter] = predefinedColors[index % predefinedColors.length];
  });

  return colorMap;
};

export const isSameColor = (color1: string, color2: string) => {
  if (color1 === '' || color2 === '') return;
  if (color1.toUpperCase() === color2.toUpperCase()) return true;
  return false;
};

export const isUpperCase = (str: string) => {
  if (!str) return false;
  return str === str.toUpperCase() && /[A-Z]/.test(str);
};
