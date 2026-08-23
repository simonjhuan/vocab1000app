# 5 แอปในโปรเจกต์นี้ — สารบัญกันงง

โปรเจกต์นี้เป็น monorepo เดียว มี 5 แอปที่ build แยกกัน โครงสร้างหน้าตาคล้ายกันมาก
(ทุกตัวใช้ webview + Capacitor) จุดประสงค์ของไฟล์นี้คือกันงงว่า "โฟลเดอร์ไหน = แอปไหน
บน Play Store"

**กฎเหล็ก: เปิดโปรเจกต์ผ่าน `เปิด-*.bat` เท่านั้น ห้ามเปิด Android Studio ตรงๆ**
เพราะแต่ละ bat จะ copy `capacitor.config.*.ts` ที่ถูกต้องไปทับ `capacitor.config.ts`
ที่ root ก่อนเปิด ถ้าเปิดตรงๆ config ที่ root อาจเป็นของแอปอื่นค้างอยู่

## ตารางแอปทั้งหมด

| ชื่อแอป (Play Store) | โฟลเดอร์ Android | โฟลเดอร์ iOS | applicationId | Launcher | Capacitor config | versionCode ล่าสุด |
|---|---|---|---|---|---|---|
| **GAT-PAT Daily Words** | `android-gatpat` | `ios-gatpat` | `com.vocab1000app` | `เปิด-GAT-PAT.bat` | `capacitor.config.gatpat.ts` | 2 |
| **Vocab M1** (ศัพท์ ม.1) | `android-M1` | `ios-M1` | `com.vocab.m1` | `เปิด-M1.bat` | `capacitor.config.m1.ts` | 2 |
| **Vocab M2** (ศัพท์ ม.2) | `android-M2` | `ios-M2` | `com.vocab.m2` | `เปิด-M2.bat` | `capacitor.config.m2.ts` | 2 |
| **Vocab M3** (ศัพท์ ม.3) | `android-M3` | `ios-M3` | ⚠️ ดูหมายเหตุ | `เปิด-M3.bat` | `capacitor.config.m3.ts` | 2 |
| **Vocab1000** (Vocab Mat Ton) | `android-vocab1000` | `ios-vocab1000` | `com.vocab1000.app` | `เปิด-Vocab1000.bat` | `capacitor.config.vocab1000.ts` | 3 |

**หมายเหตุ:** โฟลเดอร์ `ios-*` ทั้งหมด (ยกเว้น `ios-M1` ที่มีอยู่ก่อนแล้ว) ถูกสร้างเมื่อ
2026-07-30 ด้วย `npx cap add ios` — ยังไม่เคย build/sign จริง ต้องเปิดบน macOS
(Xcode) เพื่อ build ก่อน สคริปต์ `เปิด-*.bat` ปัจจุบัน sync แค่ `android` ยังไม่ได้
เพิ่มขั้นตอน sync ios ให้อัตโนมัติ

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
