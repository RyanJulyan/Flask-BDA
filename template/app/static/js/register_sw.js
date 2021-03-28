window.addEventListener('load', () => {
  registerSW();
});

async function registerSW() {
  if ('serviceWorker' in navigator) {
    try {
      await navigator.serviceWorker.register('/sw.js',{scope: "/"})
      .then(function(result){
        console.log("sw.js Scope:", result.scope)
      });
    } catch (e) {
      console.log(`SW registration failed: `,e);
    }
  }
}