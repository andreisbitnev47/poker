const dgram = require('dgram');
module.exports = class Dqn{
    constructor() {
        this.resolve = null;
        this.startServer();
        this.timeOut = null;
    }
    startServer() {
        // server
        const PORT = 33333;
        const HOST = '127.0.0.1';
        
        const server = dgram.createSocket('udp4');

        server.on('listening', function () {
            const address = server.address();
            console.log('UDP Server listening on ' + address.address + ":" + address.port);
        });

        server.on('message', function(message, remote) {
            // console.log(remote.address + ':' + remote.port +' - ' + message);
            if(this.resolve) {
                // console.log(`message - ${message} sent.`)
                clearTimeout(this.timeOut);
                this.resolve(parseInt(message))
                this.resolve = undefined;
                // this.timeOut = null;
            }
        }.bind(this));

        server.bind(PORT, HOST);
    }
    sendMessage(message, resolve, timeOut) {
        // client
        const PORT = 44444;
        const HOST = '127.0.0.1';

        const client = dgram.createSocket('udp4');
        this.resolve = resolve;
        this.timeOut = timeOut;
        client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
            // console.log(`message - ${message} sent.`)
            if (err) throw err;
            // console.log('UDP message sent to ' + HOST +':'+ PORT);
            client.close();
        });
        // this.timeOut = setTimeout(function(){
        //     if(this.resolve) {
        //         this.resolve(0)
        //     }
        // }, 500)
    }
}
