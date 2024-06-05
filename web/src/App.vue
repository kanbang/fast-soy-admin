<script setup lang="ts">
import { computed } from 'vue';
import { NConfigProvider, darkTheme } from 'naive-ui';
import { useAppStore } from './store/modules/app';
import { useThemeStore } from './store/modules/theme';
import { naiveDateLocales, naiveLocales } from './locales/naive';

defineOptions({
  name: 'App'
});

const appStore = useAppStore();
const themeStore = useThemeStore();

const naiveDarkTheme = computed(() => (themeStore.darkMode ? darkTheme : undefined));

const naiveLocale = computed(() => {
  return naiveLocales[appStore.locale];
});

const naiveDateLocale = computed(() => {
  return naiveDateLocales[appStore.locale];
});
</script>

<template>
  <NConfigProvider :theme="naiveDarkTheme" :theme-overrides="themeStore.naiveTheme" :locale="naiveLocale"
    :date-locale="naiveDateLocale" class="h-full">
    <AppProvider>
      <!--add by fs 用于给fast-crud安装naive-ui，让fs-crud拥有message notification dialog的能力-->
      <fs-ui-context>
        <RouterView class="bg-layout" />
      </fs-ui-context>
    </AppProvider>
  </NConfigProvider>
</template>

<style scoped></style>
