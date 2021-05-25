let installPrompt;

const installButton = document.querySelector('#installButton');

// hide the installButton initially
installButton.style.display = "none";

window.addEventListener('beforeinstallprompt', e => {
  e.preventDefault();
  // show the installButton if it makes sense
  if(!window.isNativeApp){
    installButton.style.display = "inline-block";
    installPrompt = e;
  }
});

installButton.addEventListener('click', () => {
  if (!installPrompt ) {
    // The deferred prompt isn't available.
    return;
  }
  
  // Show the install prompt.
  installPrompt.prompt();
  
  // Log the result
  installPrompt.userChoice.then((result) => {
    // console.log('userChoice', result);
    // Reset the deferred prompt variable, since prompt() can only be called once.
    installPrompt = null;
    // Hide the install installButton.
    installButton.style.display = "none";
  });
});