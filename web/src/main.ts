/*
 * @Descripttion: 
 * @version: 0.x
 * @Author: zhai
 * @Date: 2024-05-31 21:27:14
 * @LastEditors: zhai
 * @LastEditTime: 2024-06-10 17:13:31
 */
import { createApp } from 'vue';
import './plugins/assets';
import { setupDayjs, setupIconifyOffline, setupLoading, setupNProgress } from './plugins';
import { setupStore } from './store';
import { setupRouter } from './router';
import { setupI18n } from './locales';
import { setupFastCrud } from './plugins';
import VueResizeObserver from "vue-resize-observer";
import App from './App.vue';



async function setupApp() {
  setupLoading();

  setupNProgress();

  setupIconifyOffline();

  setupDayjs();

  const app = createApp(App);
  
  app.use(VueResizeObserver) 

  setupStore(app);

  await setupRouter(app);

  setupI18n(app);

  setupFastCrud(app);

  app.mount('#app');
}

setupApp();
