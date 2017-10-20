// vim: set expandtab tabstop=2 :

let path    = require('path');
let webpack = require('webpack');

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
                test: /\.vue$/,
                loader: 'vue-loader',
                options: {
                    // vue-loader options go here
                }
            },
            {
                test: /\.js$/,
                loader: 'buble-loader',
                exclude: /node_modules/,
                options: {
                    objectAssign: 'Object.assign'
                }
            },
            {
                test: /\.styl$/,
                loader: ['style-loader', 'css-loader', 'stylus-loader']
            }

/*
      {
        // Doesn't seem to work: handler for material icon fonts
                test: /\.(eot|svg|ttf|woff|woff2)$/,
                loader: 'file?name=node_modules/mdi/fonts/[name].[ext]'
      }
*/
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
          'SOCKETIO_BASE_URL': process.env.NODE_ENV === 'production' ? '/': 'http://localhost:5000'
        })
    ]
};

if (process.env.NODE_ENV === 'production') {
    module.exports.devtool = '#source-map';
    // http://vue-loader.vuejs.org/en/workflow/production.html
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
