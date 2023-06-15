import { StyleSheet, View } from 'react-native';
import React from 'react';
import RootStack from './src/RouteStack/RouteStack';

export default function App() {
  return (
    <View style={styles.container}>
      <RootStack />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1f1f1f',
  },
});
