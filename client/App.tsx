import { StyleSheet, Text, View } from 'react-native';
import { Grid } from './src/Grid/Grid';
import React from 'react';

export default function App() {
  const gridString = 'A3A2B3B3C1D2D3C';
  return (
    <View style={styles.container}>
      <Text
        style={{
          color: 'white',
          paddingVertical: 20,
          fontSize: 20,
          fontWeight: 'bold',
        }}>
        {gridString}
      </Text>
      <Grid gridString={gridString} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1f1f1f',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
