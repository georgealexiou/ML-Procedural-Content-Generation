import { StyleSheet, Text, View } from "react-native";
import { useGrid } from "./useGrid";
import { Cell } from "../Cell/Cell";
import { useState } from "react";

type GridProps = {
  gridString: String;
};
export const Grid: React.FC<GridProps> = ({ gridString }) => {
  const { grid, colorMap } = useGrid({
    gridString,
  });

  return (
    <View
      style={{
        flexDirection: "column",
        borderTopWidth: 10,
        borderLeftWidth: 10,
        borderColor: "black",
      }}
    >
      {grid.map((row, rowIndex) => (
        <View key={rowIndex} style={{ flexDirection: "row" }}>
          {row.map((cell, cellIndex) => (
            <Cell color={colorMap[cell]} />
          ))}
        </View>
      ))}
    </View>
  );
};
