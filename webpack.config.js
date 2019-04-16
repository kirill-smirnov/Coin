// Combined 'require' statements
const path = require('path');
const webpack = require('webpack');
const frontConfig = {
  target: "web",
  entry: {
    app: ["./src/index.js"]
  },
  output: {
    path: __dirname,
    filename: "bundle.js",
  },
  resolve: {
    extensions: ['.js', '.jsx']
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
        query: {
          cacheDirectory: true,
          presets: ['@babel/env']
        }
      }      
    ]
  },
  devServer: {
    contentBase: __dirname,
    compress: true,
    port: 3000
  }
}

module.exports = frontConfig;