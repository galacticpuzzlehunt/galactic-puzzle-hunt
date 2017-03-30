var CURRENT_USER = '';
var CHATS_DIV = null;
var HISTORY_LEN = 30;
var CHAT_HISTORY = new Array();
var hasChatted = false;
var currentBox = 0;
var rollHistory = "";

var REQUEST_URL = "/dynamic/thunk_request";
    
for (var i=0; i<HISTORY_LEN; ++i) {
	CHAT_HISTORY[i] = '';
}
    
function isNotEmpty(val) {
  if (val.match(/^\s+$/) || val == ""){
    return false;
  } else {
    return true;
  }
}
function getPlayerData() {
  var data = Cookies.get("playerData");
  return data ? data : '';
}
	
function sendChat(form) {
  updateChat("<p style=\"font-family:courier; font-size: 15px;\">&gt; " + $("#chattext").val() + "</p>");
  if (isNotEmpty($("#chattext").val())) {
    $.post(REQUEST_URL, JSON.stringify(
            {"content": $("#chattext").val(),
             "currentBox": currentBox,
             "history": rollHistory}),
            function(data) { onChatReturned(data); });
    $("#chattext").val("");
  }
}
function updateChat(data) {
  CHATS_DIV = document.getElementById("chats");
  var build_str = "";
  for (var i=0; i<HISTORY_LEN-1; ++i) {
		CHAT_HISTORY[i] = CHAT_HISTORY[i+1];
		build_str += CHAT_HISTORY[i];
  }
  CHAT_HISTORY[HISTORY_LEN-1] = data;
  build_str += CHAT_HISTORY[HISTORY_LEN-1];
  
  CHATS_DIV.innerHTML = '';
  CHATS_DIV.innerHTML += build_str;
  
  scrollToBottom();
}
	    
function onChatReturned(data) {
  var jsonData = $.parseJSON(data);
  var dataArray = jsonData["content"].split("[br]");
  for (var i=0; i<dataArray.length; ++i) {
    updateChat(dataArray[i] + "<br>");
  }
  currentBox = jsonData["currentBox"];
  rollHistory = jsonData["history"];
  $("#chattext").focus();
}

function setup() {
  CHATS_DIV = document.getElementById("chats");

  var csrftoken = Cookies.get('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!this.crossDomain) {
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  updateChat("Welcome to Thunk!<br><br>");

  $.post(REQUEST_URL, JSON.stringify(
            {"content": "look",
             "currentBox": currentBox,
             "history": rollHistory}),
      function(data) { onChatReturned(data); });
}
	
function scrollToBottom() {
  CHATS_DIV.scrollTop = CHATS_DIV.scrollHeight;
}
