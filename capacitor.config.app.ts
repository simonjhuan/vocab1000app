import type { CapacitorConfig } from '@capacitor/cli';

// Merged single app (replaces the 5 per-grade / GAT-PAT apps on iOS).
// One app, 5 word sets picked in-app (mton / m1 / m2 / m3 / gatpat).
const config: CapacitorConfig = {
  appId: 'com.simonjhuan.vocabdaily',
  appName: 'ศัพท์อังกฤษ ม.ต้น',
  webDir: 'app',
  ios: { path: 'ios/app' }
};

export default config;
