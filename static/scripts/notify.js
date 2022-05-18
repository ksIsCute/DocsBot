if (Notification.permission !== 'granted') {
  Notification.requestPermission();
};

function show() {
  console.log("notification shown")
}

function notify(message, description, icon, url) {
  if (Notification.permission !== 'granted')
    Notification.requestPermission();
  else {
      let notification = new Notification(`${message}`, {
        icon: `${icon}`,
        body: `${description}`,
        onshow: `${show()}`
    })
    notification.onclick = function() {
      console.log("clicked")
      window.open(url)
    }
  }
}