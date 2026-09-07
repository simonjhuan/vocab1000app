import type { CapacitorConfig } from '@capacitor/cli';

// Android build of the merged app (mirrors iOS's capacitor.config.app.ts).
// Reuses the live com.vocab1000.app package so the existing Play Store listing
// updates in place to the multi-set picker instead of becoming a new listing.
const config: CapacitorConfig = {
  appId: 'com.vocab1000.app',
  appName: 'เกมส์ศัพท์อังกฤษ ม.ต้น–GAT-PAT',
  webDir: 'app',
  android: { path: 'android-vocab1000' },
  ios: { path: 'ios/vocab1000' }
};

export default config;
