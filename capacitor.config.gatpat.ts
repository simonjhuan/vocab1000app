import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.vocab1000app',
  appName: 'GAT-PAT Daily Words',
  webDir: 'www',
  android: { path: 'android-gatpat' },
  ios: { path: 'ios-gatpat' }
};

export default config;
