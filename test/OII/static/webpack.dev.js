/**
 * Dev config.
 */

const HtmlWebpackPlugin = require('html-webpack-plugin');
const merge = require('webpack-merge');
const common = require('./webpack.common.js');

module.exports = merge(common, {
  mode: 'development',
  plugins: [
    new HtmlWebpackPlugin({
      title: 'Dev',
    }),
  ],
  devtool: 'inline-source-map',
  devServer: {
    contentBase: './dist',
  },
});
