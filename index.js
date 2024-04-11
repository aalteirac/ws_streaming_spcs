var http = require('http');
var fs = require('fs');
const path = require('path');
const url = require('url');
const WebSocket = require('ws')
const express = require('express');
const app = express();

app.use(express.static(path.join(__dirname, 'static')));

app.get('/', (req,res) => {
    res.sendFile(path.join(__dirname+'/index.html'));
});

const server = http.createServer(app);
server.listen(8080);
const wss = new WebSocket.Server({ server: server });

wss.broadcast = function broadcast(msg){
    wss.clients.forEach(function each(client){
        client.send(msg);
    });
  };

wss.on('connection', function connection(ws) {
    ws.on('message', function incoming(message) {
        console.log('received: %s', message);
        sendSocket(`${message}` )
    });
});  

function sendSocket(data){
    wss.broadcast(`Sending back initial msg:  ${data}`)
}         



