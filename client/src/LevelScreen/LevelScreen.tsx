import React, { useState } from 'react';
import { Text, View } from 'react-native';
import { Grid } from '../Grid/Grid';
import { SmallButton } from '../SmallButton/SmallButton';

export const LevelScreen: React.FC = () => {
  const gridString = 'A3A2B3B3C1D2D3C';
  const [reset, setReset] = useState(false);
  const [moveCount, setMoveCount] = useState(0);

  return (
    <View style={{ alignItems: 'center', justifyContent: 'center', height: '100%', backgroundColor: '#1f1f1f' }}>
      <Text
        style={{
          color: 'white',
          paddingVertical: 20,
          fontSize: 20,
          fontWeight: 'bold',
        }}>
        {gridString}
      </Text>
      <Text
        style={{
          color: 'white',
          paddingVertical: 20,
          fontSize: 20,
        }}>
        {`Moves: ${moveCount}`}
      </Text>

      <Grid gridString={gridString} reset={reset} moveCount={moveCount} setMoveCount={setMoveCount} />
      <SmallButton
        title={'Reset Grid'}
        onPress={() => {
          setReset(!reset);
        }}
      />
    </View>
  );
};
