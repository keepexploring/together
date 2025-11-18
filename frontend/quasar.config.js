const { configure } = require('quasar/wrappers');

module.exports = configure(function (ctx) {
  return {
    boot: [
      'axios',
    ],

    css: [
      'app.scss'
    ],

    extras: [
      'roboto-font',
      'material-icons',
      'material-icons-outlined',
      'mdi-v7',
    ],

    build: {
      target: {
        browser: ['es2019', 'edge88', 'firefox78', 'chrome87', 'safari13.1'],
        node: 'node16'
      },

      vueRouterMode: 'hash',

      env: {
        API_URL: ctx.dev ? 'http://localhost:8000' : 'http://localhost:8000'
      }
    },

    devServer: {
      open: true,
      port: 9000
    },

    framework: {
      config: {
        brand: {
          primary: '#2E7D32',
          secondary: '#66BB6A',
          accent: '#4CAF50',
          dark: '#1B5E20',
          positive: '#4CAF50',
          negative: '#C10015',
          info: '#2196F3',
          warning: '#FB8C00'
        }
      },

      plugins: [
        'Notify',
        'Dialog',
        'Loading'
      ]
    },

    animations: 'all',

    ssr: {
      pwa: false
    },

    pwa: {
      workboxMode: 'generateSW',
      injectPwaMetaTags: true,
      swFilename: 'sw.js',
      manifestFilename: 'manifest.json',
      useCredentialsForManifestTag: false,
    },

    cordova: {},

    capacitor: {
      hideSplashscreen: true
    },

    electron: {
      inspectPort: 5858,
      bundler: 'packager',
      packager: {},
      builder: {
        appId: 'planet-pledge'
      }
    },

    bex: {
      contentScripts: [
        'my-content-script'
      ]
    }
  }
});
