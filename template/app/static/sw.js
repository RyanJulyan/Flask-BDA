const cacheName = 'pwa-sw-v0.0.0.2';
const staticAssets = [
  './',
  './index.html',
  'https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css',
  './static/css/styles.css',
  './static/js/immortal-db.min.js',
  './static/js/register_sw.js',
  './static/js/web_share.js',
  './static/js/install_prompt.js'
];


function isEmpty(val){
  return (val === undefined || val == null || val.length <= 0) ? true : false;
}

function isJsonString(str) {
  try {
      JSON.parse(str);
  } catch (e) {
      return false;
  }
  return true;
}

self.addEventListener('install', async e => {
  const cache = await caches.open(cacheName);
  await cache.addAll(staticAssets);
  return self.skipWaiting();
});

self.addEventListener('activate', e => {
  self.clients.claim();
});

self.addEventListener('fetch', async e => {
  const req = e.request;
  const url = new URL(req.url);

  if (url.origin === location.origin) {
    e.respondWith(cacheFirst(req));
  } else {
    e.respondWith(networkAndCache(req));
  }
});

async function cacheFirst(req) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(req);
  return cached || fetch(req);
}

async function networkAndCache(req) {
  const cache = await caches.open(cacheName);
  try {
    const fresh = await fetch(req);
    await cache.put(req, fresh.clone());
    return fresh;
  } catch (e) {
    const cached = await cache.match(req);
    return cached;
  }
}

// Web Push Notifications

self.addEventListener("push", function(event) {
  if (event.data) {
    // console.log("Push event!! ", event.data.text());
    let pushData ={};
    if(isJsonString(event.data.text())){
      pushData = JSON.parse(event.data.text());
    }
    let title="Notification",body="You have a notification", badge="./static/images/icon-512.png", icon="./static/images/icon-512.png",open_url='/', vibrate = [300, 100, 400]
    if(pushData.hasOwnProperty('title')){
      if(!isEmpty(pushData.title)){
        title = pushData.title
      }
    }
    if(pushData.hasOwnProperty('body')){
      if(!isEmpty(pushData.body)){
        title = pushData.body
      }
    }
    if(pushData.hasOwnProperty('badge')){
      if(!isEmpty(pushData.badge)){
        badge = pushData.badge
      }
    }
    if(pushData.hasOwnProperty('icon')){
      if(!isEmpty(pushData.icon)){
        icon = pushData.icon
      }
    }
    if(pushData.hasOwnProperty('open_url')){
      if(!isEmpty(pushData.open_url)){
        open_url = pushData.open_url
      }
    }
    if(pushData.hasOwnProperty('vibrate')){
      if(!isEmpty(pushData.vibrate)){
        vibrate = pushData.vibrate
      }
    }
      

    let guid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
      });
    
    event.waitUntil(
      self.registration.showNotification(
          title,
          {
            tag: guid, // a unique ID
            body: body, // content of the push notification
            data: {
              from_url: 'push', // pass the current url to the notification
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
        )
    );
  } else {
    console.log("Push event but no data");
  }
});

function closeNotification(msg,evt){
  console.log(msg, evt.notification.tag, evt.notification.data);
  evt.notification.close();
}

self.addEventListener("notificationclose",function(evt){
  closeNotification("Notification closed",evt)
});

self.addEventListener("notificationclick",function(evt){
  if(evt.action == 'open'){
    evt.waitUntil(
      self.clients.matchAll({type:"window", includeUncontrolled: "true"}).then(
        function(allClients){
          for(i in allClients){
            if(allClients[i].visiblityState === "visible"){
              console.log(allClients[i]);
              return allClients[i].openWindow(evt.notification.data.open_url)
            }
          }
        })
    );
    self.clients.openWindow(evt.notification.data.open_url);
  }
  if(evt.action == 'dismiss'){
    closeNotification("Notification closed",evt);
  }

});