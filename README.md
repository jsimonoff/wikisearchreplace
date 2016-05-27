# wikisearchreplace
# Intel Body IQ, and Reference Application, for Android

This is the home of the Android Body Reference App, which shows how to 
use Intel IQs to create a fitness app. It depends upon Intel BodyIQ (which 
in turn depends on Intel CoreIQ) and Intel Cloud SDKs.

**Note:** The reference app and many of its dependencies are works in progress.
 _Information regarding usage may change._ The reference app is not 
 intended to be a full-featured physical fitness app; rather, it exists to 
 provide example code on how to use the Intel IQs.

## Getting Started

The Body IQ Reference App code is an Android Studio project. You will need
Android Studio (obtainable freely [here](https://developer.android.com/studio/index.html)).

In Android Studio, select File => Open. Navigate to `samples/reference-app`, 
 select the `build.gradle` file, and choose `Open`. After the project has 
 opened, gradle _should_ sync automatically. This process downloads third-
 party dependencies, so it takes a few minutes, and being behind a firewall 
 could cause the process to stall at this point. If gradle does not start 
 syncing automatically, it can be manually started with a button press. 
 Once gradle has finished syncing, click the run button to build the app
 and load it onto your phone. Again, this process can take a few minutes,
 and certain firewall settings can cause it to stall.
 
 ![Diagram](AS_Diagram2.png)
 
 1. Gradle messages indicating when the gradle sync has started and finished.
 2. This button starts the gradle sync process, if it was not started automatically.
 3. This is the Run button, to build and load the app onto an Android device.
 
 ## To use the app:
 
 The first time the app is used, it will ask for the user's name, gender, and 
 height & weight. A button in the app's header allows the user to switch between 
 metric and imperial units of measurement. These values are necessary for the 
 BodyIQ to calculate things like calories burned and distance travelled during
 bodily activities. If the user desires to sync their body activitiy data to 
 Google Fit or the Intel cloud, he or she can enable these features during
 initial app sign-up as well. These services have their own sign-up and login 
 processes. They can also be enabled or disabled later on, through the app's 
 `Account` tab.
 
 ### First-time device connection
 
 After launch, the app will open into the `My BodyIQ` tab. The user will need 
 to connect to an Intel wearable device. To do this, perform the following steps:
 
 1. Tap the down arrow in the upper right-hand corner to open the `Select 
 Device` menu. The first time this is done, the menu will be mainly blank.
 2. Click the `Add A Device` button, then in the next screen click `Scan 
 and Connect`. 
 3. On the next screen, any Intel wearable devices that are within bluetooth 
 range should appear in a list (this scanning and discovery process may take a 
 few seconds). Select one, then click `Connect Device`.
 4. Whenever a device is connected, it will buzz twice. Connection is often 
 complete within a few seconds, but can take as long as a minute or two. Once
 the device buzzes, click the `Got Signal` button on the "Confirm Your Device"
 dialog. 
 
 Once this process is complete, the app will return to the main interface. If
 the wearable device already contains data regarding previous bodily activities,
 information regarding these bodily activities will be displayed in the `My 
 BodyIQ` and `Activities` tabs. Any new body activities will cause the data
 in these tabs to be updated.
 
 After a device has been connected once, from then on it will appear in the 
 `Select Device` menu so the scanning and discovery process can be skipped 
 when reconnecting in the future. If multiple devices are connected, tapping 
 one of them in the `Select Device` menu will change the values in the 
 `My BodyIQ` and `Activities` tabs to display the data for the selected device.
 
 ### Connecting to devices *after* the first time
 
 If the app is closed and re-opened, previously-connected devices will be saved 
 in the `Select Device` menu, but will not be connected. To re-connect them:
 
 1. Open the `Select Device` menu, then swipe the desired device leftward. 
 This will display two buttons: one with an eye icon (which opens a `Device
 Details` screen) and another with a trashcan icon (which disconnects from 
 the device and removes it from the `Select Device` menu).
 2. Click the button with the eye icon to open a `Device Details` view. There,
 click the `Connect Device` button. 
 3. Wait for the device to buzz to signify a successful connection, then 
 click `Got Signal`. At this point you can navigate back to the `Select 
 Device` menu, select the device, and view the body data for that device.
 
 ### The System Events log
 
 In the `Device Details` screen, there is a button labelled `View System 
 Events`. This displays a log of certain important device events such as 
  crashes, low battery events, and restarts. At the time of this writing, 
  Intel wearable devices do not maintain a reliable internal clock, and 
  their internal clock is automatically synced to the correct time upon 
  connection to an Android device. This means that the exact time of a
  system event may not be known, if it happened when the device was not
  connected.
  
  ### Firmware Update
  
  In the `Device Details` screen, there is a button labelled `Firmware 
  Update`. Clicking this button opens a screen that navigates through a 
  process of:
  
  1. Inspecting the Intel cloud to see if there is a more recent firmware
  release than the firmware of the selected device. Then, if there is:
  2. Uploading that firmware and installing it to the device. This process
  currently takes approximately 10 minutes to complete.
  
  ### `My BodyIQ` tab
  
  The `My BodyIQ` tab displays sum totals of body activity data, since the 
  previous midnight, for a selected device. It displays the total steps taken,
  calories burned, approximate distance travelled, average speed, and sum
  total duration of all body activities sensed on that device. It also displays
  the current heart rate being sensed by that device. **Note:** In order to
  save battery power, many Intel wearable devices require heart rate sensing 
  to be manually enabled with a button press on the wearable device.
  
  ### `Activities` tab
  
  The `Activities` tab can be toggled to display either a list of body 
  activities or a list of sessions. When it is shown the first time after
  launching selecting a device, it shows activities by default.
  
  The activities list displays all body activities that have been
  sensed by the device in chronological order. Each item in the list 
  displays the approximate distance travelled, the duration, the time started
  and the time stopped of the activity. **Note:** Currently, the list of 
  activities includes an extra empty activity, with no duration or distance, 
  to mark the beginning of each activity. In a future version of the app, 
  these empty activities will be filtered out.
  
  Sessions are started and stopped manually by the user. When the `Start 
  Session` button is clicked, a stopwatch will begin to mark time and a 
  new item will appear in the list of sessions. When the `Stop Session` 
  button is clicked, the final distance and duration values of the session
  will be updated in that item. Sessions have no type; each session can 
  contain multiple different body activities, and the session list item 
  will display the sum total duration and distance travelled for all 
  activities over the time period. While a session is ongoing, body activities
  will continue to be added to the activities list as usual.
  
  ### `Goals` tab
  
  The `Goals` tab allows users to set daily goals. Clicking the plus button 
  in the lower right-hand corner brings up a list of goal types, and selecting
  one opens a `Set Goal` screen, where the goal target value is set. When a
  goal has been met, the user can be notified through in-app notifications, LED 
  notifications where a light on the wearable device blinks in a user-defined
  pattern, or haptic notifications where the device vibrates in a user-defined
  pattern. The desired notification types are enabled or disabled in the 
  `Set Goal` screen.
   
   The device (LED and haptic) notifications have default patterns when first 
   enabled, but these can be configured by tapping on the line where they 
   are toggled on and off. This brings up a `Define Notification` screen.
   For LED notifications, this screen lets users define new color patterns and
   set the number of times the pattern is repeated. For Haptic notifications,
   this screen lets users define new vibration patterns and the number of times
   the pattern is repeated.
   
   The `Hydration` goal type is noteworthy; it exists to provide an example
   on how to handle user events from the device. The user sets the target 
   goal number of glasses of water. Then, each time a glass of water is 
   consumed, the user should double-tap the surface of their wearable device.
   This will cause the current progress toward the goal to increment.
 
 ## Q: What are all these dependencies in `sdk/maven-repo/com/intel/wearable`?
 
 **ICSFLib** is a low-level library for interfacing with an Intel Curie 
 Wearable device. 
 
 **CoreIQ** depends on **ICSFLib**. It provides interfaces that make it easy 
 to handle all app communication to and from the device. 
 
 **BodyIQ** depends on **CoreIQ**. It makes sense of body-related messages
 coming from the device and provides easy-to-use interfaces for understanding
 and handling bodily activities sensed by the wearable device. There are two 
 variants of **BodyIQ**; one which is configured to work with Google Fit,
 and one which omits that feature.
 
 **CloudSDK** provides access to the Intel Cloud.
 
 
 
 
 

