var socket = io.connect('http://' + document.domain + ':' + location.port + '/consultants');
socket.on('connect', function(data) {
    console.log('hello');
    socket.emit('join','');
    socket.on('joined',function(data){
         console.log(data);
    });
    socket.on('question_added',function(data){
         console.log(data);
    });
});
