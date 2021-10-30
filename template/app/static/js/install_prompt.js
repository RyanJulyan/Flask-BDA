let installPrompt;

const installButtonAction = document.getElementsByClassName('pwa-install');
const installButton = document.querySelector('#installButton');
const androidInstallScreen = document.querySelector('#menu-install-pwa-android');
const iosInstallScreen = document.querySelector('#menu-install-pwa-ios');
const menuHider = document.querySelector('.menu-hider');

var isMobile = {
    Android: function() {return navigator.userAgent.match(/Android/i);},
    iOS: function() {return navigator.userAgent.match(/iPhone|iPad|iPod/i);},
    any: function() {return (true);}
};

// hide the installButton initially
installButton.style.display = "none";
// androidInstallScreen.style.display = "none";
// iosInstallScreen.style.display = "none";

window.addEventListener('beforeinstallprompt', e => {
  e.preventDefault();
  // show the installButton if it makes sense
  if(!window.isNativeApp){
    if (isMobile.Android()) {
        console.log('Android Detected');
        // androidInstallScreen.style.display = "inline-block";
        androidInstallScreen.classList.add("menu-active");
        menuHider.classList.add("menu-active");
    }
    if (isMobile.iOS()) {
        console.log('iOS Detected');
        // iosInstallScreen.style.display = "inline-block";
        iosInstallScreen.classList.add("menu-active");
        menuHider.classList.add("menu-active");
    }
    installButton.style.display = "inline-block";
    installPrompt = e;
  }
});

function installPWA(){
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
        // Hide the install installButtons.
        installButton.style.display = "none";
        if (isMobile.Android()) {
            androidInstallScreen.style.display = "none";
            menuHider.classList.remove("menu-active");
        }
        if (isMobile.iOS()) {
            iosInstallScreen.style.display = "none";
            menuHider.classList.remove("menu-active");
        }
    });
}

for(let i = 0; i < installButtonAction.length; i++){
    installButtonAction[i].addEventListener('click', installPWA);
}

menuHider.addEventListener('click', function(){
    if (isMobile.Android()) {
        androidInstallScreen.style.display = "none";
        menuHider.classList.remove("menu-active");
    }
    if (isMobile.iOS()) {
        iosInstallScreen.style.display = "none";
        menuHider.classList.remove("menu-active");
    }
});

$('.pwa-dismiss').on('click',function(){
    console.log('User Closed Add to Home / PWA Prompt')
    createCookie('Sticky_pwa_rejected_install', true, 1);
    $('body').find('#menu-install-pwa-android, #menu-install-pwa-ios, .menu-hider').removeClass('menu-active'); 
});