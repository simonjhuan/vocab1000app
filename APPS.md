# 5 แอปในโปรเจกต์นี้ — สารบัญกันงง

โปรเจกต์นี้เป็น monorepo เดียว มี 5 แอปที่ build แยกกัน โครงสร้างหน้าตาคล้ายกันมาก
(ทุกตัวใช้ webview + Capacitor) จุดประสงค์ของไฟล์นี้คือกันงงว่า "โฟลเดอร์ไหน = แอปไหน
บน Play Store"

**กฎเหล็ก: เปิดโปรเจกต์ผ่าน `เปิด-*.bat` เท่านั้น ห้ามเปิด Android Studio ตรงๆ**
เพราะแต่ละ bat จะ copy `capacitor.config.*.ts` ที่ถูกต้องไปทับ `capacitor.config.ts`
ที่ root ก่อนเปิด ถ้าเปิดตรงๆ config ที่ root อาจเป็นของแอปอื่นค้างอยู่

## ⚠️ 2026-09-02 — iOS รวมเป็นแอปเดียว (Apple แจ้ง spam)

Apple มองว่า 5 แอปนี้เป็น spam (หน้าตา/คอนเซปต์เหมือนกัน ต่างแค่ชุดคำ) จึงรวม **ฝั่ง iOS**
เป็นแอปเดียว มี dropdown เลือกชุดคำศัพท์ในแอป:

| ส่วน | ค่า |
|---|---|
| Web dir | `app/` — `app/index.html` (UI จาก `vocab1000/index.html`) + `app/data/{mton,m1,m2,m3,gatpat}.js` (โหลดทีละชุด) |
| Capacitor config | `capacitor.config.app.ts` (แยกไฟล์ ไม่ยุ่งกับ root working-copy ของฝั่ง Android) |
| iOS project | `ios/app` (คัดลอกจาก `ios/vocab1000` เดิม) |
| Bundle ID | `com.simonjhuan.vocabdaily` — register Apple แล้ว 2026-09-02 (ที่ตั้งใจไว้ `com.vocabdaily.app` โดนจองทั่วโลก) |
| ชื่อ on-device | `ศัพท์อังกฤษ ม.ต้น` (CFBundleDisplayName / Capacitor appName) |
| App Store listing | ชื่อ **ศัพท์อังกฤษ ม.ต้น–GAT-PAT**, Apple ID **6807688657** (สร้าง 2026-09-02, Prepare for Submission) — ใส่ใน `codemagic.yaml` แล้ว |
| Provisioning profile | `vocab_merged_appstore` — สร้างใน Apple portal + **อัปโหลดเข้า Codemagic แล้ว** (Personal Account → Settings → Code signing identities → iOS provisioning profiles, Reference name `vocab_merged_appstore`). Certificate จับคู่ขึ้นเขียว = ตรงกับ Codemagic identity `distribution` (cert exp 2027-07-17) |
| Codemagic | 1 workflow `vocab-ios` (ลบ `m1-ios`…`vocab1000-ios`) — profile ref `vocab_merged_appstore`, cert `distribution`, `APP_STORE_APPLE_ID: 6807688657`. บัญชี Codemagic ที่มีโปรเจกต์ = **`juanjuan0000009@gmail.com`** (Personal Account, ไม่มี team) — app id เก่า `6a91909a56eb6be4d4d98470` เข้าไม่ได้/อาจถูกลบ ให้ re-add จาก repo |
| AdMob | AdMob app **`ศัพท์อังกฤษ ม.ต้น–GAT-PAT (iOS)`** (console app 1551618292). App id `ca-app-pub-5804107706055854~1551618292` → `ios/app/App/App/Info.plist`. Banner unit `ca-app-pub-5804107706055854/7716686913` → `app/index.html` `CONFIG.iosBannerId`, `isTesting:false`. Android ids ใน `CONFIG` ยังเป็น Google TEST (ไม่มี Android build ใช้ `app/` ตอนนี้) — เปลี่ยน + สร้าง AdMob app Android ตอน merge Android. ยังไม่มี iOS interstitial unit (โค้ดข้าม interstitial บน iOS อยู่แล้ว) |
| per-set history | `localStorage['vocab_v1:<setId>']` แยกคะแนนต่อชุด; ชุดที่เลือกล่าสุดอยู่ที่ `localStorage['vocab_set']` |

**ยังไม่แตะฝั่ง Android:** `android-*/`, `capacitor.config.{m1,m2,m3,gatpat,vocab1000}.ts`,
`เปิด-*.bat`, `vocab1000/`, `www/`, `vocab_by_grade/` คงเดิมทุกอย่าง (เป็น source of truth
ของชุดคำที่ extract มาไว้ใน `app/data/`)

**Setup ก่อน build (ทำแล้ว 2026-09-02):** App ID register, ASC app record (Apple ID 6807688657),
provisioning profile `vocab_merged_appstore` อัปโหลดเข้า Codemagic, AdMob app + banner unit,
ค่าทั้งหมดใส่ลงไฟล์แล้ว (`codemagic.yaml`, `capacitor.config.app.ts`, `ios/app/**`, `app/index.html`)

**เหลือทำเอง:**
1. Codemagic → re-add แอปนี้จาก repo (workflow `vocab-ios`) แล้ว Start new build → TestFlight
   — ตรวจ integration `codemagic_api_key` (App Store Connect API key) ยังเชื่อมอยู่
2. **หลังแอปรวมผ่านรีวิว** → เอา 5 แอปเดิมออกจาก App Store (App Store Connect →
   Pricing and Availability → Remove from sale)
3. ตอน merge ฝั่ง Android ทีหลัง: สร้าง AdMob app แยกสำหรับ Android + แทน TEST ids ใน
   `app/index.html` `CONFIG.androidBannerId`/`androidInterstitialId`

ตารางข้างล่างนี้ยังเป็นสถานะ **ฝั่ง Android + iOS เดิม (ก่อนรวม)** — เก็บไว้อ้างอิง

## ตารางแอปทั้งหมด

| ชื่อแอป (Play Store) | โฟลเดอร์ Android | โฟลเดอร์ iOS | applicationId (Android) | Bundle ID (iOS) | Launcher | Capacitor config | versionCode ล่าสุด |
|---|---|---|---|---|---|---|---|
| **GAT-PAT Daily Words** | `android-gatpat` | `ios/gatpat` | `com.vocab1000app` | ⚠️ `com.gatpat.dailywords` (คนละตัวกับ Android) | `เปิด-GAT-PAT.bat` | `capacitor.config.gatpat.ts` | 2 |
| **Vocab M1** (ศัพท์ ม.1) | `android-M1` | `ios/M1` | `com.vocab.m1` | `com.vocab.m1` | `เปิด-M1.bat` | `capacitor.config.m1.ts` | 2 |
| **Vocab M2** (ศัพท์ ม.2) | `android-M2` | `ios/M2` | `com.vocab.m2` | `com.vocab.m2` | `เปิด-M2.bat` | `capacitor.config.m2.ts` | 2 |
| **Vocab M3** (ศัพท์ ม.3) | `android-M3` | `ios/M3` | `com.vocab.moo3` ⚠️ | `com.vocab.m3` | `เปิด-M3.bat` | `capacitor.config.m3.ts` | 2 |
| **Vocab1000** (Vocab Mat Ton) | `android-vocab1000` | `ios/vocab1000` | `com.vocab1000.app` | `com.vocab1000.app` | `เปิด-Vocab1000.bat` | `capacitor.config.vocab1000.ts` | 3 |

**GAT-PAT iOS bundle id ≠ Android:** iOS ใช้ `com.gatpat.dailywords` (ตั้งใน `ios/gatpat/App/App.xcodeproj`
เท่านั้น) เพื่อเลี่ยงชนสายตากับ `com.vocab1000.app` ของ Vocab1000 — ส่วน Android/Play ยังเป็น
`com.vocab1000app` เหมือนเดิม `capacitor.config.gatpat.ts` `appId` ยังเป็น `com.vocab1000app`
(Capacitor ไม่ยุ่งกับ `PRODUCT_BUNDLE_IDENTIFIER` ใน pbxproj หลังสร้างโปรเจกต์แล้ว จึงไม่ชนกัน)

**หมายเหตุ:** โปรเจกต์ iOS ทั้ง 5 ตัวย้ายมารวมไว้ใต้โฟลเดอร์เดียว `ios/` แล้ว
(2026-08-28) เพื่อกันสับสนกับโฟลเดอร์ `android-*` ที่ root — เช่น `ios/M1`, `ios/gatpat`
เดิมชื่อ `ios-M1`, `ios-gatpat` เอกสาร/สคริปต์เก่าที่อ้าง `ios-*` ให้เข้าใจว่าหมายถึง
`ios/*` ตัวเดียวกัน ค่า `ios.path` ใน `capacitor.config.*.ts` และ `XCODE_PROJECT` ใน
`codemagic.yaml` แก้ให้ตรงพาธใหม่แล้ว

โฟลเดอร์เหล่านี้ (ยกเว้น `ios/M1` ที่มีอยู่ก่อนแล้ว) ถูกสร้างเมื่อ 2026-07-30 ด้วย
`npx cap add ios` — ยังไม่เคย build/sign จริง ต้องเปิดบน macOS (Xcode) เพื่อ build ก่อน
รัน `npx cap sync ios` บน macOS ครั้งแรกจะ regenerate `App/CapApp-SPM/Package.swift`
(ไฟล์นี้ Capacitor เป็นคนจัดการเอง) ให้พาธ relative ไป `node_modules` ถูกต้องตามตำแหน่ง
ใหม่ สคริปต์ `เปิด-*.bat` ปัจจุบัน sync แค่ `android` ยังไม่ได้เพิ่มขั้นตอน sync ios ให้อัตโนมัติ

## ⚠️ จุดที่เคยงง / ต้องระวังเป็นพิเศษ

### 1. `com.vocab1000app` (ไม่มีจุด) ≠ `com.vocab1000.app` (มีจุด)
สอง applicationId นี้หน้าตาเกือบเหมือนกัน แต่เป็นคนละแอปกันจริง:
- `com.vocab1000app` → **GAT-PAT Daily Words** (โฟลเดอร์ `android-gatpat`)
- `com.vocab1000.app` → **Vocab1000** (โฟลเดอร์ `android-vocab1000`)

ยืนยันจากการ dump APK ที่ดาวน์โหลดจาก Play Store จริง (2026-07-29): package
`com.vocab1000app` บน Play Store **ใช้ชื่อ listing ว่า "Vocab1000"** (ไม่ใช่
"GAT-PAT" อย่างที่โค้ดตอนนี้เป็น) — แปลว่าแอปนี้เคยถูกเปลี่ยนเนื้อหา/ชื่อจาก
Vocab1000 ตัวแรกมาเป็น GAT-PAT ภายหลัง โดยใช้ applicationId เดิม ก่อนอัปโหลดบิลด์
ใหม่ไปทับ listing เดิม **ให้เช็ก Play Console ก่อนว่าชื่อ listing ปัจจุบันคืออะไร**
ไม่งั้นเสี่ยงโดน reject เพราะเนื้อหาไม่ตรงกับของเดิม

### 2. `android-M3` — applicationId ไม่ตรงกันระหว่างไฟล์
- `android-M3/app/build.gradle` → `com.vocab.moo3`
- `capacitor.config.m3.ts` → `com.vocab.m3`

ไม่ได้แก้ให้ตรงกันเองเพราะไม่รู้ว่าตัวไหนคือตัวที่ publish จริงบน Play Store —
เปลี่ยนผิดจะกลายเป็นสร้างแอปใหม่ไปคนละตัวกับที่มีอยู่ **เช็ก Play Console ก่อนว่า
package จริงคืออะไร แล้วแก้ไฟล์ที่ผิดให้ตรง** (ปกติ `cap sync` จะไม่ทับ
applicationId ใน build.gradle เอง ปัญหานี้เลยไม่โผล่ตอน build ปกติ — จะโผล่ก็ต่อเมื่อ
ลบโฟลเดอร์แล้วรัน `cap add android` ใหม่)

### 3. โฟลเดอร์ `android/` เดิม (ก่อน 2026-07-29) เคยเป็นทั้ง Vocab1000 และ GAT-PAT
ก่อนหน้านี้โฟลเดอร์ชื่อ `android/` เฉยๆ (ไม่มีคำต่อท้าย) ถูกใช้ซ้ำเป็นทั้งสองแอป
คนละช่วงเวลา ตอนนี้เปลี่ยนชื่อเป็น `android-gatpat/` แล้วเพื่อไม่ให้ชื่อกำกวมอีก —
ถ้าเจอเอกสาร/สคริปต์เก่าที่อ้างถึง path `android` เฉยๆ ให้รู้ว่าหมายถึง GAT-PAT

## หมายเหตุทางเทคนิค: `capacitor.config.ts` ที่ root
ไฟล์นี้คือ "working copy" ที่ถูกทับด้วย `เปิด-*.bat` ทุกครั้งที่เปิดแอปใดแอปหนึ่ง —
เนื้อหาข้างในตอนนี้จะเป็นของแอปล่าสุดที่เปิด ไม่ใช่ค่าคงที่ อย่ายึดเป็นหลักว่าแอปไหน
"active" ให้ดูจากว่าเพิ่งรัน `เปิด-*.bat` ตัวไหนแทน

## AdMob banner (เพิ่ม 2026-08-28)

ทั้ง 5 แอปมี AdMob banner (native) ผ่าน `@capacitor-community/admob` — **ซ่อน 15 วันแรก
นับจากติดตั้ง** (เก็บ timestamp ใน localStorage `admob_install_ts`) แล้วค่อยโชว์
ADAPTIVE_BANNER ที่ล่างจอ เปิดบนเว็บ/ไม่มีปลั๊กอิน = no-op

**ใช้ id จริงจาก AdMob console แล้ว (2026-08-28)** — สร้าง 10 AdMob apps + 10 banner
units (Android+iOS อย่างละ 5) publisher id `ca-app-pub-5804107706055854`
`CONFIG.isTesting = false` ทุกไฟล์แล้ว id 3 จุดต่อแอป:

| id | ไฟล์ |
|---|---|
| Android App ID (`~`) | `android-<app>/app/src/main/AndroidManifest.xml` → `com.google.android.gms.ads.APPLICATION_ID` |
| iOS App ID (`~`) | `ios/<app>/App/App/Info.plist` → `GADApplicationIdentifier` |
| Banner unit (`/`) Android+iOS | `<webdir>/index.html` → `CONFIG.androidBannerId` / `CONFIG.iosBannerId` |

AdMob จะขึ้นสถานะ "ต้องตรวจสอบ / Verify app" จนกว่าแต่ละแอปจะเผยแพร่บนสโตร์และยืนยัน
listing — ระหว่างนั้นโฆษณาจริงอาจว่าง/จำกัด เป็นเรื่องปกติ

**ผลกระทบต่อ Store:** AdMob เพิ่ม permission `AD_ID` บน Android อัตโนมัติ → ต้องอัปเดต
Play Console → Data safety (เก็บ Advertising ID) และ App Store → App Privacy ก่อนส่งอัปเดต

**แก้พลอยได้:** `vocab1000/index.html` เดิมเรียก `../capacitor.js` (พาธผิด อยู่ที่ web root
ต้องเป็น `capacitor.js`) — แก้แล้ว มิฉะนั้นปลั๊กอิน Capacitor (รวม TTS + AdMob) ไม่โหลด
ในแอป Vocab1000

### หน่วยโฆษณาเพิ่มเติม — Vocab1000 (Android) เท่านั้น (2026-09-01)

สร้างเพิ่มใน AdMob console ใต้แอป **Vocab1000 (Android)** (`~9700441758`):

| ชื่อ unit ใน AdMob | รูปแบบ | Ad unit id |
|---|---|---|
| `Banner v2` | แบนเนอร์ | `ca-app-pub-5804107706055854/4059377460` |
| `Interstitial` | คั่นระหว่างหน้า | `ca-app-pub-5804107706055854/1832564178` |

- `vocab1000/index.html` → `CONFIG.androidBannerId` เปลี่ยนจาก `.../1369314146` (unit เดิมชื่อ
  `Banner`) มาเป็น `Banner v2` แล้ว — unit เดิมยังไม่ได้ลบ ยังอยู่ใน console เฉยๆ
- **จังหวะการแสดง (แก้ 2026-09-01):** banner แสดงตลอด — เอา grace 15 วันออกแล้ว
  (`hideDays` / `admob_install_ts` ถูกลบทิ้ง) ส่วน interstitial เด้ง **อย่างมาก 3 วัน/ครั้ง**
  (`interstitialDays: 3`) นับจาก timestamp ใน localStorage `admob_interstitial_ts` ซึ่งเขียน
  เฉพาะตอนที่โฆษณาขึ้นจริง (โหลดไม่สำเร็จไม่เผาโควต้า 3 วัน) — เด้งหลังโหลดหน้าเสร็จ 4 วินาที
  **ติดตั้งใหม่จะรอ 3 วันก่อนถึงเด้งครั้งแรก** (เปิดแอปครั้งแรก = seed timestamp แล้วไม่แสดง)
- interstitial รันเฉพาะ Android — iOS ข้ามเพราะยังไม่ได้สร้าง unit ไว้
- iOS ยังไม่ได้แตะ: `CONFIG.iosBannerId` ยังเป็น `.../1686220367` และแอป Vocab1000 (iOS)
  ยังมี unit เดียวเหมือนเดิม
- ไฟล์ `android-vocab1000/app/src/main/assets/public/index.html` กับ
  `ios/vocab1000/App/App/public/index.html` เป็น build output ยังค้าง id ตัวเก่า/TEST อยู่ —
  จะอัปเดตเองตอนรัน `เปิด-Vocab1000.bat` (`npx cap sync android`)
