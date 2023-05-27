import { View } from "react-native";

type CellProps = {
  color: string;
};

export const Cell: React.FC<CellProps> = ({ color }) => {
  return (
    <View
      style={{
        width: 60,
        height: 60,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: color,
        borderRightWidth: 10,
        borderBottomWidth: 10,
        opacity: color ? 1 : 0.5,
      }}
    />
  );
};
