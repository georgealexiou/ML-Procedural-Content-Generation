import { StyleSheet, Text, View } from "react-native";
import { useGrid } from "./useGrid";

type GridProps = {
  gridString: String;
};
export const Grid: React.FC<GridProps> = ({ gridString }) => {
  const { gridSize, grid } = useGrid({ gridString });

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
        <View
          key={rowIndex}
          style={{
            flexDirection: "row",
          }}
        >
          {row.map((cell, cellIndex) => (
            <View
              key={cellIndex}
              style={{
                height: 50,
                width: 50,
                backgroundColor: cell ? cell : "white",
                alignItems: "center",
                justifyContent: "center",
                borderBottomWidth: 10,
                borderRightWidth: 10,
              }}
            >
              <Text style={{ fontSize: 20, color: "white" }}>{cell}</Text>
            </View>
          ))}
        </View>
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  gridContainer: {
    flexDirection: "column",
  },
  rowContainer: {
    flexDirection: "row",
  },
  cell: {
    width: 40,
    height: 40,
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 1,
    borderColor: "black",
  },
  cellText: {
    fontSize: 18,
  },
});
