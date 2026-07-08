@echo off
echo กำลังเปิด ศัพท์ ม.1 ...
cd /d "D:\AndroidStudioProjects\vocab1000app"
copy /y capacitor.config.m1.ts capacitor.config.ts >nul
npx cap sync android
start "" "C:\Program Files\Android\Android Studio\bin\studio64.exe" android-M1
