@echo off
echo กำลังเปิด ศัพท์ ม.3 ...
cd /d "D:\AndroidStudioProjects\vocab1000app"
copy /y capacitor.config.m3.ts capacitor.config.ts >nul
npx cap sync android
start "" "C:\Program Files\Android\Android Studio\bin\studio64.exe" android-M3
