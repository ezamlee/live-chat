
//$(document).ready(function((){

var webSocket;
console.log("webSocket")
//try to add args
webSocket= new WebSocket("ws://localhost:1234/ws");
	console.log(webSocket)

$(function(){
	
	//$("#LOM").append(LOM)
	//$("#LOM").append(groupId)
	var x= document.getElementById("group");
	var selected;
	webSocket.onopen = function(e){
		//var x =prompt("name");
		//
		$.ajax({
		method: 'get',
		async: true,
		url: 'http://localhost:5888/',
		data: {userId: x, gId: , class: },
		success: function(res){
			console.log(res);
}
})
	}
	webSocket.onmessage = function(e){
		console.log(e.data);
		$("#chat-body").append("<p>"+e.data+"</p>");
		
	}
	var msg = $("#message").val()
