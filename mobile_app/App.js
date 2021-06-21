import React, {Component, useState} from 'react';
import { 
    StyleSheet,
    View,
    Text,
    Image,
    Dimensions,
    ActivityIndicator,
    TouchableHighlight
} from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import NetInfo from '@react-native-community/netinfo';
import AsyncStorage from '@react-native-community/async-storage';
import { WebView } from 'react-native-webview';
import {server_base_url} from './app.json';
// import { View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';

let current_screen = 'Init';
let is_connected = true;
const dimensions = Dimensions.get('window');
// const imageHeight_3_6x1 = Math.round(dimensions.width * 1 / 3.6);
// const imageWidth_3_6x1 = dimensions.width;

const Stack = createStackNavigator();

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        backgroundColor:'#ffffff'
    },
    webview: {
        flex: 1,
        backgroundColor:'#ffffff'
    },
    logo_image: {
        marginTop: 150,
        height: 200,
        width:200
    },
    icon_image: {
        marginTop: 150,
        height: 200,
        width:200
    },
    button: {
        marginRight:40,
        marginLeft:40,
        marginTop:10,
        paddingTop:20,
        paddingBottom:20,
        backgroundColor:'#fff',
        borderRadius:10,
        borderWidth: 1,
        borderColor: "#d7d7d7",
        borderStyle: "solid",
        overflow: 'hidden',
        width:100
    },
    submitText:{
        color:'#6e6e6e',
        textAlign:'center',
    }
});

async function requestExternalApi(method,url,post_body_obj,callback) {
    try {
        return fetch(url,{
            method: method,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(post_body_obj),
        })
            .then((response) => response.json())
            .then((json) => {
                let data_obj = this.getJsonObject(json);
                if (typeof data_obj.Result !== "undefined") {
                    if (data_obj.Result === "Success") {
                        callback(data_obj);
                    } else {
                        callback({"Error": data_obj});
                    }
                } else {
                    callback({"Error": data_obj});
                }
            })
            .catch((error) => {
                callback({"Error": error});
                console.error(error);
            });
    } catch (error) {
    
    }
}

async function registerDevice(success_callback,failed_callback) {
    try {
    device_token = await AsyncStorage.getItem('device_token');
    success_callback(device_token)
    // try {
    //     device_token = await AsyncStorage.getItem('device_token');
    //     requestExternalApi("POST",server_base_url+'/api/auth/registerDevice',
    //         {
    //             AuthenticationToken: device_token,
    //             DeviceUuid:DeviceInfo.getUniqueId(),
    //             DevicePlatform:DeviceInfo.getDeviceId(),
    //             DeviceOs:DeviceInfo.getSystemName()
    //         },
    //         async function(data_obj) {
    //             if (typeof data_obj.Error !== "undefined") {
    //                 failed_callback();
    //                 return;
    //             }
    //             if (data_obj.Result === "Success") {
    //                 authentication_token = data_obj.DeviceLinkedAuthenticationToken;
    //                 await AsyncStorage.setItem('device_token', data_obj.device_token);
    //                 success_callback(device_token);
    //                 return;
    //             }
    //             failed_callback();
    //         });
        
    } catch (error) {
        failed_callback();
    }
}

async function registerPushNotifications(success_callback,failed_callback) {
    console.log("TODO: Put your code that asks for push notification permissions here. Once a successful Push" +
        " registration ID is received, send it to the server with");
    //this.createPushRegistration("The ID received from the push service",success_callback,failed_callback);
}

const setFirstLaunchTag = async first_launch_tag => {
    try {
        await AsyncStorage.setItem('first_launch', first_launch_tag);
    } catch (error) {}
};

const checkFirstLaunch = async ({navigation}) => {
    let first_launch;
    try {
        first_launch = await AsyncStorage.getItem('first_launch');
    } catch (error) {}
    if (first_launch == null) {
        loadScreenByName({navigation},'Welcome');
    } else {
        loadScreenByName({navigation},'Web');
    }
    
    NetInfo.addEventListener(state => {
        if (!state.isConnected && is_connected) {
            loadScreenByName({navigation},'Offline');
        } else if (state.isConnected && !is_connected) {
            loadScreenByName({navigation},current_screen);
        }
        is_connected = state.isConnected;
    });
};

function loadScreenByName({navigation}, screen_name) {
    let screen_loaded = screen_name;
    if (screen_name === "Web") {
        NetInfo.fetch().then(state => {
            if (state.isConnected) {
                screen_loaded = 'Web';
            } else {
                screen_loaded = 'Offline';
            }
        });
        
        loadScreenAsReset({navigation},screen_loaded);
    } else {
        loadScreenAsReset({navigation},screen_loaded);
    }
    if (screen_loaded !== 'Offline') {
        current_screen = screen_loaded;
    }
}

function loadScreenAsReset({navigation}, screen_name) {
    navigation.reset({
        index: 0,
        routes: [
            {
                name: screen_name
            },
        ],
    });
    // React.useRef(null).current.navigate(screen_name)
}


function InitScreen({navigation}) {
    checkFirstLaunch({navigation});
    return (
        <>
            <StatusBar style="dark" />
            <View style={styles.container}>
                <Image
                    style={styles.logo_image}
                    source={require('./assets/icon.png')} />
                <Text style={styles.heading}>Initializing...</Text>
                <View style={styles.bottom}>
                    <TouchableHighlight
                        style={styles.button}
                        onPress={() => loadScreenByName({navigation},'Web')}
                        underlayColor='#d7d7d7'>
                        <Text style={styles.submitText}>Force Load</Text>
                    </TouchableHighlight>
                </View>
            </View>
        </>
    );
}

function LoadingScreen({navigation}) {
    return (
        <>
            <StatusBar style="dark" />
            <View style={styles.container}>
                <LoadingIndicator/>
            </View>
        </>
    );
}

function LoadingIndicator() {
    return <ActivityIndicator
        color="#3367D6"
        visible = {true}
        textContent={'Loading...'}
        style={{ position: 'absolute', left: 0, right: 0, bottom: 0, top: 0, }}
        size="large"
    />
}

function WelcomeScreen({navigation}) {
    return (
        <>
            <StatusBar style="dark" />
            <View style={styles.container}>
                <Image
                    style={styles.logo_image}
                    source={require('./assets/icon.png')} />
                <Text style={styles.heading}>WELCOME</Text>
                <Text style={styles.text}>This is the default welcome screen for a Flask BDA native app. It will only show once.</Text>
                <Text style={styles.text}>This is useful for introducing your app to the user and to inform the user that they will always require an internet connection and that certain requests for permissions might follow (i.e Push notifications)</Text>
                <View style={styles.bottom}>
                    <TouchableHighlight
                        style={styles.button}
                        onPress={() => confirmWelcomeScreen({navigation})}
                        underlayColor='#d7d7d7'>
                        <Text style={styles.submitText}>Next</Text>
                    </TouchableHighlight>
                </View>
            </View>
        </>
    );
}

function confirmWelcomeScreen({navigation}) {
    loadScreenByName({navigation},"Loading");
    registerDevice(
        function() {
            setFirstLaunchTag("1");
            loadScreenByName({navigation},'Web');
            registerPushNotifications(function() {
                //Success
            },function() {
                //failed
            });
        },
        function() {
            loadScreenByName({navigation},"Error");
        }
    )
}

function OfflineScreen({navigation}) {
    return (
        <>
            <StatusBar style="dark" />
            <View style={styles.container}>
                <Image
                    style={styles.icon_image}
                    source={require('./assets/offline.png')} />
                <Text style={styles.heading}>YOU'RE OFFLINE</Text>
                <Text style={styles.text}>Please check your internet connection to proceed</Text>
                <View style={styles.bottom}>
                    <TouchableHighlight
                        style={styles.button}
                        onPress={() => loadScreenByName({navigation},'Web')}
                        underlayColor='#d7d7d7'>
                        <Text style={styles.submitText}>Retry</Text>
                    </TouchableHighlight>
                </View>
            </View>
        </>
    );
}

function ErrorScreen({navigation}) {
    return (
        <>
            <StatusBar style="dark" />
            <View style={styles.container}>
                <Image
                    style={styles.icon_image}
                    source={require('./assets/warning.png')} />
                <Text style={styles.heading}>ERROR</Text>
                <Text style={styles.text}>Please check your internet connection to proceed</Text>
                <View style={styles.bottom}>
                    <TouchableHighlight
                        style={styles.button}
                        onPress={() => loadScreenByName({navigation},'Web')}
                        underlayColor='#d7d7d7'>
                        <Text style={styles.submitText}>Retry</Text>
                    </TouchableHighlight>
                </View>
            </View>
        </>
    );
}

function WebScreen({navigation}) {
    const [visible, setVisible] = useState(false);
    const runFirst = `
      window.isNativeApp = true;
      true; // note: this is required, or you'll sometimes get silent failures
    `;
    return (
        <>
            <StatusBar style="dark" />
            <SafeAreaView style={styles.webview}
                          forceInset={{bottom: 'never'}}>
                <WebView
                    style={{ marginTop: 5 }}
                    startInLoadingState={true}
                    source={{ uri: server_final_url }}
                    // renderLoading={() => {
                    //     return LoadingIndicator();
                    // }}
                    // onMessage={(event)=> receiveMessageFromWeb(event)}
                    onLoadStart={() => (setVisible(true))}
                    onLoad={() => setVisible(false)}
                    
                    //Enable Javascript support
                    javaScriptEnabled={true}
                    //For the Cache
                    domStorageEnabled={true}
                    injectedJavaScriptBeforeContentLoaded={runFirst}
                />
                {visible ? LoadingIndicator() : null}
            </SafeAreaView>
        </>
    );
}

class FlaskBDAWebAppWrapper extends Component{

    render() {
        return (
            <NavigationContainer>
                <Stack.Navigator
                    screenOptions={{
                        headerShown: false
                    }}
                    initialRouteName={current_screen}
                >
                        <Stack.Screen 
                            name="Init" 
                            component={InitScreen}
                            options={{title: 'Init', animationEnabled: true}}
                        />
                        <Stack.Screen
                            name="Welcome"
                            component={WelcomeScreen}
                            options={{title: 'Welcome'}}
                        />
                        <Stack.Screen 
                            name="Loading" 
                            component={LoadingScreen}
                            options={{title: 'Loading', animationEnabled: true}}
                        />
                        <Stack.Screen 
                            name="Offline" 
                            component={OfflineScreen}
                            options={{title: 'Offline', animationEnabled: false}}
                        />
                        <Stack.Screen
                            name="Error"
                            component={ErrorScreen}
                            options={{title: 'Error'}}
                        />
                        <Stack.Screen 
                            name="Web"
                            component={WebScreen} 
                            options={{title: 'Web',animationEnabled: false}}
                        />
                </Stack.Navigator>
            </NavigationContainer>
        );
    }
}


// let stored_auth_token = await AsyncStorage.getItem('main_authentication_token');
let server_final_url = server_base_url+"?view=native_landing&init_native=1";
// console.log(server_final_url)

export default class App extends React.Component {
  render() {
    return (
    
    <View style={{ flex: 1 }}>
        <FlaskBDAWebAppWrapper/>
    </View>
    );
  }
}
