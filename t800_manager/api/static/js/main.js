function get_device_id(){
  const device_id = document.getElementById('deviceHeader').getAttribute('device_id')
  return device_id
}

function fetch_page(id){
  var device_id = get_device_id()
  var main = document.getElementById('board');
  var page = id.getAttribute('name')
  main.innerHTML = `<div class=loader><center><div class="lds-dual-ring"></div></center></div>`
  fetch(`/${device_id}/page`, {
      method: "POST",
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: `name=${page}`
    }).then(response => response.text().then(function (text){
      main.innerHTML = text;
    }
    ))
}

function fetch_screen(){
  var device_id = get_device_id()
  var main = document.getElementById('currentScreen');
  fetch(`/${device_id}/getScreen`, {
      method: "GET"
    }).then(response => response.text().then(function (text){
      main.innerHTML = text;
    }
    ))
}


function sendCMD(id){
  var device_id = get_device_id()
  input = id.children[1].children[0]
  if(input.value === 'clear'){
    document.getElementById('stdout_pre').innerText = '';
    input.value = ''
  }else{
  fetch(`/${device_id}/cmd`, {
    method: "POST",
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: `cmd=${input.value}`
  }).then(response => response.text().then(
    function (text){
      document.getElementById('stdout_pre').innerText = text;
    }
  ))
  input.value = ''}


  
}

function debug_device(device){
  var device_id = device.getAttribute('device_id')
  document.location = `/${device_id}/`
}