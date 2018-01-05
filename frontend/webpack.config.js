// vim: set expandtab tabstop=2 :

const path = require('path')
const webpack = require('webpack')

module.exports = {
  entry: './src/main.js',
  output: {
    path: path.resolve(__dirname, './dist'),
    publicPath: '/dist/',
    filename: 'build.js'
  },
  resolve: {
    alias: {
      'public': path.resolve(__dirname, './public')
    }
  },
  module: {
    rules: [
      {
        test: /\.(js|vue)$/,
        loader: 'eslint-loader',
        enforce: 'pre',
        // include: [resolve('src'), resolve('test')],
        options: {
          formatter: require('eslint-friendly-formatter')
        }
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          preLoaders: {
            i18n: 'yaml-loader'
          },
          loaders: {
            i18n: '@kazupon/vue-i18n-loader'
          }
        }
      },
      {
        test: /\.ya?ml$/,
        loader: 'js-yaml-loader'
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.css$/,
        use: [ 'style-loader', 'css-loader' ]
      },
      {
        test: /\.styl$/,
        loader: ['style-loader', 'css-loader', 'stylus-loader']
      },
      {
        test: /\.(eot|svg|ttf|woff|woff2)$/,
        loader: 'file-loader?name=public/fonts/[name].[ext]'
      }
    ]
  },
  devServer: {
    historyApiFallback: true,
    noInfo: true,
    compress: true,
    disableHostCheck: true
  },
  devtool: '#eval-source-map',
  plugins: [
    new webpack.EnvironmentPlugin({
      'URL_ROOT': process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:5000',
      'SOCKETIO_BASE_URL': process.env.NODE_ENV === 'production' ? '/' : 'http://localhost:5000'
    }),
      new webpack.ProvidePlugin({
          $: "jquery",
          jQuery: "jquery"
      })
  ]
}

if (process.env.NODE_ENV === 'production') {
  module.exports.devtool = '#source-map'
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        warnings: false
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    })
  ])
}
