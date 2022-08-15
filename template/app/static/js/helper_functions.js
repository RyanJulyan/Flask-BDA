

function guid() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
  var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

function isEmpty(val){
  return (val === undefined || val == null || val.length <= 0) ? true : false;
}

function IsJsonString(str) {
  try {
      JSON.parse(str);
  } catch (e) {
      return false;
  }
  return true;
}

function toggle_password_visibility(id) {
    var inp = document.getElementById(id);
    var icon = document.getElementById(id+"_icon");
    if (inp.type === "password") {
        inp.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        inp.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
}

function xor_encrypt_decrypt(message, key_string){
    let key = key_string.split("");
    let output = [];
    for (let i = 0; i < message.length; i++){
        char_code = (message[i].charCodeAt(0)) ^ key[i % key.length][0].charCodeAt(0);
        output.push(String.fromCharCode(char_code));
    }
    return output.join("");
}
