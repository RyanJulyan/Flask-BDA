# Flask-BDA
Flask-BDA is built using a Flask Rapid Application Development (RAD) called [Flask-BDA](https://github.com/RyanJulyan/Flask-BDA/).

# Know how to style a MD document properly
[https://www.markdownguide.org/basic-syntax/](https://www.markdownguide.org/basic-syntax/)

## React Native

> For native mobile apps we are using react native, specifically we are using [expo](https://expo.io/) a framework and a platform for universal React applications. It is a set of tools and services built around React Native and native platforms that help you develop, build, deploy, and quickly iterate on iOS, Android, and web apps from the same JavaScript/TypeScript codebase.

> Advantages include faster build and testing workflows/processes, remote testing while developing with Over The Air (OTA) updates with changes visible on save during development.

> However there are some disadvantages and [Limitations](https://docs.expo.io/introduction/why-not-expo/) Expo is aware of these and describes them quite well. we suggest reviewing these limitations before using our pre-built method.

> Build one project that runs natively on all your users' devices.

## Install Expo
* Open a browser and install node.js:
    * Go to: [https://nodejs.org/en/download/](https://nodejs.org/en/download/)
    * Follow the installation instructions and then continue to the next steps

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
cd <Path To>/my_awesome_project_mobile_app

npm install -g expo-cli

npm install

```

### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
cd <Path To>/my_awesome_project_mobile_app

npm install -g expo-cli

npm install

```

### Changing the App URL

> Because Flask BDA does not dictate where you should host your website, you will need to tell your Mobile App where to go.

> In the quickstart example we created a project called `"My Awesome Project"`, however, you may have called the project something else.
> This would have created a folder where the name is all in lower case and will have stripped out all of the special characters and replaced spaces with underscores eg: `my_awesome_project`.

> For mobile we will have automatically created a separate `"_mobile_app"` folder where the prefix of the folder is your project name eg `my_awesome_project_mobile_app`. This is to prevent issues with the `Serverless` configuration `package.json` and allow you to not have to deploy all the code for a mobile app onto your web server.


#### run local instance on Public URL with ngrok

> If you are still in development and/or have not chosen a service provider for hosting yet, you could use: [Ngrok](https://ngrok.com/) to create a temporary public development URL that tunnels to your local environment. Ngrok exposes local servers behind NATs and firewalls to the public internet over secure tunnels. This allows you to demo websites on a public URL and test mobile apps connected to your locally running backend, without deploying.

* Start the local development server by following the [Local Environment](#local-environment) instructions

* If you have not registered for ngrok before:
    * Open a browser and register for ngrok:
        * Go to: [https://dashboard.ngrok.com/signup](https://dashboard.ngrok.com/signup)
        * Follow the installation instructions and then continue to the next steps
* If you have already registerd but do not have it installed:
    * Open a browser and register for ngrok:
        * Go to: [https://dashboard.ngrok.com/get-started/setup](https://dashboard.ngrok.com/get-started/setup)
        * download the correct version for your OS and run the application.
* Once the ngrok terminal is open, create a tunnel from your local server to ngrok
    * create the tunnel to ngrok from the:
        * If you have changed the port number from the default `5000`, then replace ths number after `http` to allow for the correct tunnel to be created.
    
```shell
ngrok http 5000

```

* This should return a randomly generated URL that you can now use for testing eg:
```shell
ngrok by @inconshreveable
(Ctrl+C to quit) 
Session Status                online
Session Expires               1 hour, 59 minutes
Version                       2.3.40
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://573d4ec93267.ngrok.io -> http://localhost:5000
Forwarding                    https://573d4ec93267.ngrok.io -> http://localhost:5000

Connections
ttl     opn     rt1     rt5     p50     p90
0       0       0.00    0.00    0.00    0.00

```

> **Note:** the free version only keeps this server alive for 2 hours, so you may need to follow this process in the future and if you push this URL to your "Repo", it may not work for the next person.


#### Update the mobile App URL

* Open the Mobile App folder `my_awesome_project_mobile_app`
    * Once open, select the `app.json` file and edit line 2 `"server_base_url": "https://github.com/RyanJulyan/Flask-BDA"` by replacing `https://github.com/RyanJulyan/Flask-BDA` with your own server name.

### Run App
* Install the `expo` App on your own mobile phone by searching for "expo" on the Apple or Google Play Store:
    * `iOS` Go to: [https://apps.apple.com/app/apple-store/id982107779](https://apps.apple.com/app/apple-store/id982107779)
    * `Android` Go to: [https://play.google.com/store/apps/details?id=host.exp.exponent](https://play.google.com/store/apps/details?id=host.exp.exponent)

> Once you have the app installed on your phone you can start a development server on your local machine.

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
cd <Path To>/my_awesome_project_mobile_app

expo start

```

### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
cd <Path To>/my_awesome_project_mobile_app

expo start

```

> This will open a webpage with a QR code on it. This will allow you to use the Expo app if you are on Android or use the camera if you are on iOS to scan the code and open your app directly from the development server.

> **Note:** if you wish for people not on your network to be able to scan and test the App remotely; press the `tunnel` tab button above the QR code.

### Deploying to stores
* Open browser and review expo's recommendations to ensure you are ready to deploy:
    * Go to:https://docs.expo.io/distribution/app-stores/
* Open browser and review expo's recommendations on building for the different platforms:
    * Go to:https://docs.expo.io/distribution/building-standalone-apps/

> Part of the recommendations are to ensure that images are optimized. To do this expo has recommended the [expo-optimize package](https://github.com/expo/expo-cli/tree/master/packages/expo-optimize#-welcome-to-expo-optimize) which can assist with optimizing images. Optimizing images can noticeable improve your native app TTI (or time-to-interaction) which means less time on splash screens and quicker delivery over poor network connections

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
cd <Path To>/my_awesome_project_mobile_app

npm install -g sharp-cli

npx expo-optimize --quality 0.9

```

### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
cd <Path To>/my_awesome_project_mobile_app

npm install -g sharp-cli

npx expo-optimize --quality 0.9

```

# License

## Expo Framework

View license information for the Expo Framework and other legal agreements (https://github.com/expo/expo/blob/master/LICENSE).

It is the user's responsibility to ensure that adhere to the Acceptable Use Policy (https://app.serverless.com/legal/aup)

________________________________________

## The Flask-BDA License

Flask-BDA is created and distributed under the developer-friendly Flask-BDA License. The Flask-BDA License is derived from the popular Apache 2.0 license.

The Flask-BDA License is the legal requirement for you or your company to use and distribute Flask-BDA and derivative works such as the applications you make with it. Your application or project can have a different license, but it still needs to comply with the original one.

### The license grants you the following permissions:
* You are free to commercialize any software created using original or modified (derivative) versions of Flask-BDA
* You are free to commercialize any plugin, extension, or tool created for use with Flask-BDA
* You are free to modify Flask-BDA and you are not required to share the changes
* You are free to distribute original or modified (derivative) versions of Flask-BDA
* You are given a license to any patent that covers Flask-BDA

### The license prevents you from doing the following:
* You can not commercialize original or modified (derivative) versions of the Flask-BDA editor, creator and/or engine
* You can not hold Flask-BDA or Ryan Julyan liable for damages caused by the use of Flask-BDA
* You can not bring any warranty claims to Flask-BDA or Ryan Julyan
* You can not use the Flask-BDA trademark unless express permission has been given (see exceptions and additional information)
The license requires that you do the following:
    * You must include the Flask-BDA license and copyright notice in any work you create
    * You must state significant changes made to Flask-BDA

License and copyright notice inclusion

The Flask-BDA License requires that you must include the license and copyright notice with all copies of Flask-BDA and in any derived work created using Flask-BDA. It is up to you to decide how you wish to distribute the license and notice. Below are some examples of how this can be done:
* Show the license and notice at the end of a credits screen if your application has one
* Show the license and notice from a dedicated license screen or popup in your application
* Print the license and notice to an output log when your application starts
* Put the license and notice in a text file and include it with the distribution of your application
* Put the license and notice in a printed manual included with your application

________________________________________

Copyright 2021 Flask-BDA, Ryan Julyan
Licensed under the Flask-BDA License version 0.1 (the "License"); you may not use `Flask-BDA` except in compliance with the License.
You may obtain a copy of the [License](https://github.com/RyanJulyan/Flask-BDA/blob/main/LICENSE), at
[`https://github.com/RyanJulyan/Flask-BDA/blob/main/LICENSE`](https://github.com/RyanJulyan/Flask-BDA/blob/main/LICENSE)
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
