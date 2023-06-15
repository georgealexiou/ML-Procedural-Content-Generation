import React from 'react';
import { Pressable, Text, View } from 'react-native';
import { Grid } from '../Grid/Grid';
import { SmallButton } from '../SmallButton/SmallButton';

export const HomeScreen: React.FC = ({ navigation }) => {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: '#1f1f1f' }}>
      <SmallButton
        title={'Generate Level'}
        onPress={() => {
          navigation.navigate('Level');
        }}
      />
    </View>
  );
};
