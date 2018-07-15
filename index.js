const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const config = require('./config');

const app = express();

app.use(bodyParser.json());

if(config.buildMode === 'production') {
    app.use('/', express.static(path.join(__dirname, './src/dist')));
} else if(config.buildMode === 'development') {
    const webpackMiddleware = require('webpack-dev-middleware');
    const webpack = require('webpack');
    const webpackConfig = require('./webpack.config.js');
    app.use(webpackMiddleware(webpack(webpackConfig)));
}

app.post('/update', (req, res) => {
    const {reward, data} = req.body;
    const spawn = require("child_process").spawn;
    const pythonProcess = spawn('python',["./ai.py", reward, ...data]);
    pythonProcess.stdout.on('data', (data) => {
        res.status(200).json({
            message: 'Success',
            data: String.fromCharCode.apply(null, data)
        });
    });
});

app.listen(4000, () => {
  console.log('Server running on port 4000');
});