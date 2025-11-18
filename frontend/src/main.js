import { createApp } from 'vue'
import { Quasar, Notify, Dialog, Loading } from 'quasar'
import iconSet from 'quasar/icon-set/material-icons'
import '@quasar/extras/material-icons/material-icons.css'
import '@quasar/extras/material-icons-outlined/material-icons-outlined.css'
import '@quasar/extras/mdi-v7/mdi-v7.css'
import 'quasar/dist/quasar.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(Quasar, {
  plugins: {
    Notify,
    Dialog,
    Loading
  },
  iconSet: iconSet,
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
  }
})

app.use(router)

app.mount('#q-app')
