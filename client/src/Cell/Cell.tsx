import React from 'react';
import { useState } from 'react';
import { ColorValue, Pressable, View } from 'react-native';

type CellProps = {
  color: ColorValue;
  currentColor: ColorValue;
  setCurrentColor: React.Dispatch<React.SetStateAction<ColorValue>>;
};

export const Cell: React.FC<CellProps> = ({ color, currentColor, setCurrentColor }) => {
  const [highlightedColor, setHighlightedColor] = useState<ColorValue | undefined>();
  return (
    <Pressable
      style={{
        width: 60,
        height: 60,
        justifyContent: 'center',
        alignItems: 'center',
        borderRightWidth: 10,
        borderBottomWidth: 10,
      }}
      onPress={() => {
        console.log(color, ' + ', currentColor, ' + ', highlightedColor);
        if (color) {
          setCurrentColor(color);
          return;
        }

        if (currentColor) {
          setHighlightedColor(currentColor);
        }
      }}>
      {highlightedColor ? (
        <View
          style={{
            backgroundColor: highlightedColor,
            height: '100%',
            aspectRatio: 1,
            opacity: 0.3,
          }}
        />
      ) : (
        <View
          style={{
            backgroundColor: color,
            height: '100%',
            aspectRatio: 1,
          }}
        />
      )}
    </Pressable>
  );
};
