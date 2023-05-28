import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  cellPressable: {
    width: 60,
    height: 60,
    justifyContent: 'center',
    alignItems: 'center',
    borderRightWidth: 10,
    borderBottomWidth: 10,
  },
  node: {
    height: '100%',
    aspectRatio: 1,
  },
  connection: {
    height: '100%',
    aspectRatio: 1,
    opacity: 0.3,
  },
});
