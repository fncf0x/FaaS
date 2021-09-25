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

function refresh_devices(){
  var devices_list = document.getElementById('devices_list');
  devices_list.innerHTML = `<br><br><center><div class="lds-dual-ring"></div></center>`
  fetch('/devices', {
      method: "GET"
    }).then(response => response.text().then(function (text){
      devices_list.innerHTML = text;
    }
    ))
}

function show_panel(){
  var panel = document.getElementById('add_device_panel');
  var container = document.getElementById('container');
  var devices = document.getElementById('devices');
  panel.style.opacity = "1"
  panel.style.zIndex = "999"
  
  container.style.zIndex = "0"
  devices.style.opacity = "0.2"
}
function hide_panel(){
  var panel = document.getElementById('add_device_panel');
  var container = document.getElementById('container');
  var devices = document.getElementById('devices');
  panel.style.opacity = "0"
  panel.style.zIndex = "0"
  
  container.style.zIndex = "999"
  devices.style.opacity = "1"
}

function stopped(device){
  var device_id = device.getAttribute('device_id')
  var status = document.getElementById(`${device_id}_stopped`);
  status.innerHTML = '<center><div class="lds-dual-ring-small"></div></center>'
  fetch('/start_device', {
    method: "POST",
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: `id=${device_id}`
  }).then(response => response.text().then(
    function (text){
      status.innerHTML = 'booting'
      status.className = 'device_booting'
    }
  ))
}

function running(device){
  var device_id = device.getAttribute('device_id')
  var status = document.getElementById(`${device_id}_running`);
  status.innerHTML = '<center><div class="lds-dual-ring-small"></div></center>'
  fetch('/pause_device', {
    method: "POST",
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: `id=${device_id}`
  }).then(response => response.text().then(
    function (text){
      status.innerHTML = 'stopped'
      status.className = 'device_stopped'
      refresh_devices()
    }
  ))  
}

function remove(device){
  var device_id = device.getAttribute('device_id')
  fetch('/delete_device', {
    method: "POST",
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: `id=${device_id}`
  }).then(response => response.text().then(
    function (text){
      refresh_devices()
    }
  ))  
}

function add(){
  hide_panel()
  var image_name = document.getElementById('image_name')
  fetch('/add_device', {
    method: "POST",
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: `image_name=${image_name.value}`
  }).then(response => response.text().then(
    function (text){
      refresh_devices()
    }
  ))  
}