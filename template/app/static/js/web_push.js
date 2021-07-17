let webPushPrompt;

const webPushButton = document.querySelector('#webPushButton');

// console.log(webPushButton);

// hide the webPushButton initially
webPushButton.style.display = "none";

if(window.Notification){
  
  webPushPrompt = window.Notification;
  
  if (webPushPrompt.permission !== 'granted') {
    webPushButton.style.display = "inline-block";
  }
  else{
    webPushButton.style.display = "none";
  }

};

webPushButton.addEventListener('click', () => {
  
  if (!webPushPrompt ) {
    // The deferred prompt isn't available.
    return;
  }
  
  // Show the request to send prompt.
  requestWebPushPermission();
});

function requestWebPushPermission(){
  
  webPushPrompt.requestPermission().then(permission => {
    if (permission !== 'granted') {
      alert('you need to allow push notifications');
      webPushButton.style.display = "inline-block";
    }
    else{
      webPushButton.style.display = "none";
    }
  });

}

function subscribeToPush(){
  
  if (!webPushPrompt ) {
    // The deferred prompt isn't available.
    return;
  }
  
  if (webPushPrompt.permission !== 'granted') {
    requestWebPushPermission();
    return;
  }
  
  navigator.serviceWorker.ready.then(function(reg){
    reg.pushManager.subscribe({userVisibleOnly:true}).then(function(sub){
      console.log(sub)
      console.log(sub.endpoint)
    });
  });
}

function showWebNotification(title="Notification",body="You have a notification", badge="./static/images/icon-512.png", icon="./static/images/icon-512.png",open_url='/', vibrate = [300, 100, 400]){
  
  if (!webPushPrompt ) {
    // The deferred prompt isn't available.
    return;
  }
  
  if (webPushPrompt.permission !== 'granted') {
    requestWebPushPermission();
    return;
  }

  let guid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  
  navigator.serviceWorker.ready.then(function(reg){
      reg.showNotification(
      title,
      {
        tag: guid, // a unique ID
        body: body, // content of the push notification
        data: {
          from_url: window.location.href, // pass the current url to the notification
          timestamp: Date.now(),
          open_url: open_url
        },
        badge: badge,
        icon: icon,
        actions: [
          {
            action: 'open',
            title: 'Open'
          },
          {
            action: 'dismiss',
            title: 'Dismiss',
          }
        ],
        vibrate:vibrate
      }
    );
  })
}
  
