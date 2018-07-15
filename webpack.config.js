const path = require("path");
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    mode: 'development',
    devtool: 'source-map',
    entry: ['babel-regenerator-runtime', './src/index.js'],
    output: {
        path: path.resolve(__dirname, 'src/dist'),
        filename: 'bundle.js'
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: 'public/index.html'
        })
    ],
    module: {
        rules: [
          {
            test: /\.js$/,
            exclude: /node_modules/,
            use: [
              'babel-loader',
            ]
          },
          {
            test: /\.css$/,
            use: [
              {
                loader: 'style-loader'
              }, 
              {
                loader: 'css-loader',
                options: {
                  importLoaders: 1,
                  modules: true
                }
              }
            ]
          }
        ]
      },
      resolve: {
        extensions: ['.js', '.jsx'],
      }
}