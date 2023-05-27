const calculateGridSize = (gridString: string): number => {
  let totalCells = 0;
  [...gridString].forEach((character) => {
    totalCells += isNaN(parseInt(character)) ? 1 : parseInt(character);
  });

  return Math.floor(Math.sqrt(totalCells));
};

const parseStringToGrid = (gridString: String, gridSize: number): Grid => {
  const grid: Grid = [];
  let row: (string | null)[] = [];

  [...gridString].forEach((character) => {
    if (isNaN(parseInt(character))) {
      row.push(character);
    } else {
      const spaces = Array(parseInt(character)).fill(null);
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

export const useGrid = ({ gridString }: { gridString: String }) => {
  const gridSize = calculateGridSize(gridString);
  const grid = parseStringToGrid(gridString, gridSize);
  console.log(gridSize, " ", grid);
  return { gridSize, grid };
};
