const fs = require('fs');
module.exports = class Dqn{
    update(reward, data) {
        return new Promise((resolve, reject) => {
            const spawn = require("child_process").spawn;
            const pythonProcess = spawn('python',["./ai.py", reward, ...data]);
            let log = `reward: ${reward}, data: ${data}, `;
            pythonProcess.stdout.on('data', (resp) => {
                const response = parseInt(String.fromCharCode.apply(null, resp));
                log += 'action: ' + response + '\n'
                // fs.appendFile('/home/andrei/projects/poker/logs.txt', log, function (err) {
                //     if (err) throw err;
                //     console.log(log);
                //     resolve(response)
                // });
                console.log(log);
                resolve(response)
            });
        });
    }
}