@echo off
echo กำลังเปิด GAT-PAT Daily Words ...
cd /d "D:\AndroidStudioProjects\vocab1000app"
copy /y capacitor.config.gatpat.ts capacitor.config.ts >nul
npx cap sync android
start "" "C:\Program Files\Android\Android Studio\bin\studio64.exe" android
