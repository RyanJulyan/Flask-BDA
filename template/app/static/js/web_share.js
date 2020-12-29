  
const shareButtons = document.querySelectorAll('.shareButton');

if (navigator.share) {
  
  const defaultTitle = 'Default Example PWA';
  const defaultText = 'This is a bare bones example of a PWA with all the features I want to include';
  const defaultUrl = 'https://pwadvent.dev/';
  
  for (i = 0; i < shareButtons.length; i++) {

    shareButtons[i].addEventListener('click', (e) => {
      let title = e.path[0].dataset.title ? e.path[0].dataset.title : defaultTitle;
      let text = e.path[0].dataset.text ? e.path[0].dataset.title : defaultText;
      let url = e.path[0].dataset.url ? e.path[0].dataset.title : defaultUrl;
      
      navigator.share({
        title: title,
        text: text,
        url: url,
      })
      .then(() => console.log('Successful share'))
      .catch((error) => console.log('Error sharing', error));

    });

  }
  
}
else{
  
  for (i = 0; i < shareButtons.length; i++) {
    // hide the shareButtons if webshare not supported
    shareButtons[i].style.display = "none";
  }
  
}