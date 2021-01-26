import * as React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { WebView } from 'react-native-webview';
import {server_base_url} from './app_config.json';
// import { View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';


const styles = StyleSheet.create({
  webview: {
      flex: 1,
      backgroundColor:'#fff'
  }
});

// let stored_auth_token = await AsyncStorage.getItem('main_authentication_token');
let server_final_url = server_base_url+"?view=native_landing&init_native=1";
// console.log(server_final_url)
export default class App extends React.Component {
  render() {
    return (
      <SafeAreaView style={styles.webview}>
        {/* other code here to show the screen */}
  
        {/* use light text instead of dark text in the status bar to provide more contrast with a dark background */}
        <StatusBar style="dark" />
        <WebView source={{ uri: server_final_url }} style={{ marginTop: 20 }} />
      </SafeAreaView>
    );
  }
}
