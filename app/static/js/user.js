$(function(){
	$('select').dropdown();
});
var socket = io.connect('http://' + document.domain + ':' + location.port + '/users');
socket.on('connect', function(data) {
    console.log('hello');
    socket.on('answer_added',function(data){
         console.log(data);
    });
});
