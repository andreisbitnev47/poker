const fs = require('fs');
const Udp = require('./udp');
module.exports = class Dqn{
    constructor() {
        this.udp = new Udp()
    }
    update(reward, data) {
        return new Promise((resolve, reject) => {
            const timeOut = setTimeout(function() {
                reject();
            }, 500);
            // const spawn = require("child_process").spawn;
            // const pythonProcess = spawn('python',["./ai.py", reward, ...data]);
            // let log = `reward: ${reward}, data: ${data}, `;
            // pythonProcess.stdout.on('data', (resp) => {
            //     const response = parseInt(String.fromCharCode.apply(null, resp));
            //     log += 'action: ' + response + '\n'
            //     console.log(log);
            //     resolve(response)
            // });
            const message = JSON.stringify([reward, ...data]);
            this.udp.sendMessage(message, resolve, timeOut)
        });
    }
    save() {
        return new Promise((resolve, reject) => {
            const timeOut = setTimeout(function() {
                reject();
            }, 500);
            this.udp.sendMessage('save', resolve)
        })
        
    }
}