@echo off
echo กำลังเปิด ศัพท์ ม.ต้น 1000 คำ ...
cd /d "D:\AndroidStudioProjects\vocab1000app"
copy /y capacitor.config.vocab1000.ts capacitor.config.ts >nul
npx cap sync android
start "" "C:\Program Files\Android\Android Studio\bin\studio64.exe" android-vocab1000
