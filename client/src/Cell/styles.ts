import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  cellPressable: {
    width: 60,
    height: 60,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 5,
  },
  node: {
    height: '100%',
    aspectRatio: 1,
    borderRadius: 10,
  },
  connection: {
    height: '100%',
    aspectRatio: 1,
    opacity: 0.3,
    borderRadius: 10,
  },
});
