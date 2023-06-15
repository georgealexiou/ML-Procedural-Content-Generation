import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { HomeScreen } from '../HomeScreen/HomeScreen';
import { LevelScreen } from '../LevelScreen/LevelScreen';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

export default function RootStack() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Main" component={Main} options={{ headerShown: false }} />
        <Stack.Screen name="Level" component={LevelScreen} options={{ headerShown: false }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const Main = () => {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarShowLabel: false,
      }}>
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{
          headerShown: false,
        }}
      />
    </Tab.Navigator>
  );
};
