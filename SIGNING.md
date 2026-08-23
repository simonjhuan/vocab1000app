# นโยบายเซ็นแอป iOS — บัญชี Sutee Sodsai (736T54Z9Z8)

> เอกสารนี้ **ก๊อปวางไว้ทุก repo** ที่ใช้บัญชี Apple นี้
> Tether Me · moneyhunterpro · PetGuardian Pro · EduTrack · CarCare Pro ·
> My Health Book · family-os · Life is
>
> **ต้นฉบับอยู่ที่ `github.com/simonjhuan/life-is` → `SIGNING.md`**
> แก้ที่นั่นที่เดียว แล้วก๊อปทับตัวอื่น — อย่าแก้แยกในแต่ละ repo ไม่งั้น
> จะกลับไปเป็นปัญหาเดิมคือไม่รู้ว่าฉบับไหนถูก

เอกสารนี้เป็น **วิธีป้องกัน** ไม่ใช่วิธีกู้ ถ้าทำตามนี้ทุกโปรเจกต์ ปัญหา
certificate โดน revoke จะไม่เกิดขึ้นอีกเลย

---

## ต้นเหตุ — ทำไมมันวนไม่จบ

Apple ให้ **Apple Distribution certificate ได้แค่ 3 ตัวต่อบัญชี** พอสร้างตัวที่ 4
Apple จะ revoke ตัวเก่าสุดทิ้ง**ทันทีโดยไม่ถาม**

บัญชีนี้มี 8 โปรเจกต์ใช้ร่วมกัน ถ้าโปรเจกต์ไหนตั้งเป็น **automatic signing**
พอ build แล้วหา certificate ที่ใช้ได้ไม่เจอ มันจะสร้างใหม่ให้เอง แล้ววงจรนี้ก็เริ่ม:

```
โปรเจกต์ A build → automatic signing สร้าง cert ใหม่
                 → Apple เต็ม 3/3 → revoke ตัวเก่าสุด
                 → B, C, D พังพร้อมกัน
                 → B กด generate ใหม่ → revoke ตัวเก่าสุดอีก
                 → A พัง ... วนไปเรื่อย ๆ
```

**ทุกครั้งที่ "แก้" คือการจุดชนวนรอบถัดไป** นี่คือเหตุผลที่แก้เท่าไหร่ก็ไม่จบ

---

## กฎ — จำแค่บรรทัดเดียว

> **Certificate มีได้ 3 · Provisioning profile มีได้ไม่จำกัด**

เพราะฉะนั้น:

- ใช้ **certificate ตัวเดียว** ร่วมกันทั้ง 8 โปรเจกต์
- แต่ละโปรเจกต์มี **provisioning profile ของตัวเอง** (สร้างกี่อันก็ได้ ไม่กระทบใคร)
- **ปิด automatic signing ทุกโปรเจกต์**

พอไม่มีโปรเจกต์ไหนสร้าง certificate ได้อีก ก็ไม่มีอะไรไป revoke ใครได้

```
                   ┌── Tether Me       profile
                   ├── moneyhunterpro  profile
Apple Distribution ├── PetGuardian Pro profile
cert  ×1  ─────────┼── EduTrack        profile
หมดอายุ 17 ก.ค. 2027├── CarCare Pro     profile
                   ├── My Health Book  profile
                   ├── family-os       profile
                   └── Life is         profile
```

---

## 🚫 ห้ามทำ

| ห้าม | ที่ไหน |
|---|---|
| กด **Generate certificate** | Codemagic → Code signing identities |
| กด **+** ในหน้า Certificates | developer.apple.com |
| ใส่ `--create-certificate` / `fetch-signing-files --create` ใน script | `codemagic.yaml` |

ปุ่ม **Fetch certificate** ของ Codemagic **ปลอดภัย** — มันดึงเฉพาะของที่มีอยู่แล้ว
ไม่สร้างอะไรใหม่ (และดึงได้เฉพาะ cert ที่ Codemagic เป็นคนสร้างเอง เพราะ
มันต้องมี private key)

### `distribution_type` + `bundle_identifier` ไม่ใช่ของต้องห้าม

```yaml
ios_signing:
  distribution_type: app_store
  bundle_identifier: com.company.appname
```

รูปแบบนี้ **ไม่สร้าง certificate ใหม่** ตราบใดที่มี provisioning profile ของ
bundle ID นั้นอัปโหลดอยู่ใน Code signing identities แล้ว — Codemagic แค่หยิบ
profile กับ cert ที่มีอยู่มาใช้ ยืนยันแล้วจากผล build จริงของ family-os และ
Life is (`ARCHIVE SUCCEEDED` / `EXPORT SUCCEEDED`)

**ลำดับสำคัญ: อัปโหลด profile ก่อน แล้วค่อย build** ถ้า build ทั้งที่ยังไม่มี profile
นั่นแหละคือตอนที่มันจะไปสร้างของใหม่ให้

> คอมเมนต์เก่าในไฟล์ `carcarepro/codemagic.yaml` เขียนห้ามรูปแบบนี้ไว้ — ตอนนี้
> รู้แล้วว่าเข้มเกินจริง สาเหตุจริงของการ revoke คือ **build ตอนที่ยังไม่มี profile**
> ไม่ใช่ตัวไวยากรณ์นี้

---

## ย้ายโปรเจกต์เดิมมาใช้นโยบายนี้

ทำทีละโปรเจกต์ ทำครั้งเดียวจบ ไม่ต้องรีบ — ทำตอนที่โปรเจกต์นั้น build ผ่านอยู่

**1 · ออก provisioning profile ของโปรเจกต์นั้น**

developer.apple.com → Profiles → **+** → Distribution → App Store Connect
→ เลือก App ID ของโปรเจกต์ → เลือก **certificate ตัวที่ใช้ร่วมกัน** →
ตั้งชื่อ `[ชื่อโปรเจกต์] AppStore v1` → Generate → Download

**2 · Upload เข้า Codemagic**

Codemagic → Personal Account → Settings → Code signing identities →
iOS provisioning profiles → Upload

reference name: `[ชื่อโปรเจกต์]-appstore-profile-v1` (พิมพ์เล็ก ขีดกลาง)

หน้านี้เป็น **ระดับบัญชี** ใช้ร่วมกันทุกแอป ไม่ใช่ตั้งต่อแอป

**3 · ปิด automatic signing — ขั้นตอนที่สำคัญที่สุด**

ถ้าโปรเจกต์ตั้งค่าผ่าน UI: App settings → Distribution → iOS code signing →
เปลี่ยนจาก **Automatic** เป็น **Manual** → เลือก profile จากข้อ 2

ถ้าตั้งค่าผ่าน `codemagic.yaml` และต้องการระบุไฟล์แบบเจาะจง ใช้บล็อกนี้

```yaml
environment:
  ios_signing:
    provisioning_profiles:
      - ชื่อ-profile-จากข้อ-2
    certificates:
      - ชื่อ-certificate-ที่ใช้ร่วมกัน
```

แล้วใน `scripts:` ใช้ `xcode-project use-profiles` เท่านั้น
**ห้ามใช้** `app-store-connect fetch-signing-files --create-certificate`

สำหรับโปรเจกต์ที่ใช้รูปแบบเดียวกับ `family-os` สามารถให้ Codemagic เลือก
profile/certificate ที่อัปโหลดไว้แล้วตาม bundle ID ได้:

```yaml
integrations:
  app_store_connect: Codemagic Admin
environment:
  ios_signing:
    distribution_type: app_store
    bundle_identifier: com.lifeis.diary
```

รูปแบบนี้ไม่สร้าง certificate ใหม่ แต่ยังต้องมี profile ของ bundle ID นี้อยู่ใน
Code signing identities ก่อนเริ่ม build

**4 · Build ยืนยัน** ว่าผ่าน แล้วค่อยไปโปรเจกต์ถัดไป

---

## โปรเจกต์ใหม่

ทำข้อ 1–3 ข้างบน ไม่ต้องแตะ certificate เลยแม้แต่นิดเดียว

ก่อนออก profile ต้องมี App ID ก่อน:
developer.apple.com → Identifiers → **+** → App IDs → App →
Bundle ID แบบ Explicit

> ติ๊ก Capabilities เท่าที่**จำเป็นจริง** เท่านั้น
> Local Notifications (`UNUserNotificationCenter`) **ไม่ต้องใช้** Push Notifications
> ถ้าติ๊กไปจะต้องมี APNs key ตามมาโดยเปล่าประโยชน์

---

## ตอน certificate หมดอายุ — 17 กรกฎาคม 2027

นี่คือ**ครั้งเดียวที่ได้รับอนุญาตให้สร้าง certificate ใหม่** และต้องทำแบบตั้งใจ
ไม่ใช่ทำเพราะ build พัง

1. ลบ certificate เก่าที่หมดอายุออกจาก developer.apple.com ให้เหลือช่องว่าง
2. สร้างใหม่ **หนึ่งตัว** จาก Codemagic (Generate certificate) เพื่อให้ Codemagic
   ถือ private key
3. **ออก provisioning profile ใหม่ให้ครบทั้ง 8 โปรเจกต์** ด้วย cert ตัวใหม่นั้น
   ตั้งชื่อ `... v2`
4. Upload ทั้ง 8 อันเข้า Codemagic แล้วแก้ `codemagic.yaml` ของแต่ละ repo

ทำวันเดียวจบทั้ง 8 ตัว อย่าทยอยทำ ไม่งั้นจะมีบางตัวค้างอยู่กับ cert เก่า

---

## อ่าน error ให้ออก

| ข้อความ | แปลว่า | ทำยังไง |
|---|---|---|
| `Signing certificate is invalid ... revoked or expired` | มีคนไปสร้าง cert ใหม่ แล้ว revoke ตัวนี้ทิ้ง | หาว่าโปรเจกต์ไหนตั้ง automatic อยู่ แล้วปิดมัน จากนั้นออก profile ใหม่ |
| `No signing certificate found` / `doesn't include signing certificate` | profile อ้าง cert ที่ Codemagic ไม่มี private key | ออก profile ใหม่โดยเลือก cert อีกตัว |
| `No matching profiles` | ยังไม่มี profile หรือ bundle ID ไม่ตรง | สร้างแล้วอัปโหลด profile |
| `Cannot determine the Apple ID from Bundle ID` | **signing ผ่านแล้ว** ติดที่ยังไม่มี App record ใน App Store Connect หรือ API key มองไม่เห็นแอป | สร้างแอปใน App Store Connect · เช็คว่า key มีสิทธิ์อย่างน้อย App Manager |
| `App name already being used` | ชื่อในสโตร์ซ้ำกับแอปอื่นทั้งโลก | ตั้งชื่อสโตร์ให้ยาวและเฉพาะขึ้น — **ไม่ต้องแก้ `CFBundleDisplayName`** ชื่อใต้ไอคอนบนเครื่องยังเป็นชื่อสั้นได้ |
| `train version closed for new build submissions` | `MARKETING_VERSION` ซ้ำกับที่ Apple อนุมัติไปแล้ว | **เปิด App Store Connect ดูเวอร์ชัน live จริง** อย่าเชื่อเลขใน error — เคยพลาดมาแล้วเพราะ error บอก train `1.0` แต่ของจริง live อยู่ `2.0` |
| `missing export compliance` | ไม่มีคีย์ในตัว Info.plist | เพิ่ม `ITSAppUsesNonExemptEncryption = false` |
| `Another build is in review` | ไม่ใช่บั๊ก | รอ build ก่อนหน้าใน TestFlight review ให้เสร็จ |

### 🔑 กฎที่ประหยัดเวลาที่สุด

> **เห็น `ARCHIVE SUCCEEDED` และ `EXPORT SUCCEEDED` เมื่อไหร่ → certificate กับ
> profile ไม่ใช่ปัญหาแล้ว หยุดแก้ signing ทันที ไปดูขั้น Publishing ต่อ**

เวลาส่วนใหญ่ที่เสียไปกับเรื่องนี้ คือการกลับไปรื้อ signing ทั้งที่มันผ่านไปแล้ว
แล้วการรื้อนั้นเองที่ทำให้ certificate โดน revoke รอบใหม่

**ยืนยันสาเหตุก่อนแก้เสมอ:** Codemagic → โหลด build artifacts `.zip` → unzip →
ค้นคำว่า `error:` ใน `App.log` — หน้าสรุป build **ไม่แสดง**
`Signing certificate is invalid` มันซ่อนอยู่ในล็อกเท่านั้น

---

## ชื่อที่ต้องใช้จริงใน codemagic.yaml

อ่านมาจาก Tether Me กับ carcarepro ที่ build ผ่านอยู่ — **อย่าคิดชื่อใหม่เอง**

```yaml
integrations:
  app_store_connect: APP_STORE_CONNECT_KEY   # ห้ามมีช่องว่างในชื่อ
environment:
  ios_signing:
    certificates:
      - distribution                          # ← ตัวเดียวกันทั้ง 8 แอป
    provisioning_profiles:
      - [ชื่อโปรเจกต์]-appstore-profile-v1     # ← ของใครของมัน
```

`certificates: - distribution` คือชื่อ reference เดียวที่ถูกต้อง ถ้าเห็น
`tetherme-distribution-v2` หรือชื่ออื่นในไฟล์เก่า แปลว่านั่นคือตัวที่โดน revoke ไปแล้ว

## สถานะปัจจุบัน — กรกฎาคม 2026

- Team `736T54Z9Z8` มี Apple Distribution **2 ตัว** ทั้งคู่ชื่อ `Sutee Sodsai (Distribution)` หมดอายุ **17 ก.ค. 2027**
- เหลือช่องว่าง 1 ช่อง — **อย่าไปใช้มัน** เก็บไว้เป็นกันชนตอนต่ออายุ
- `tetherme-distribution-v2` โดน revoke ไปแล้วเมื่อ **24 ก.ค. 2026** จากการสร้าง cert ใหม่
- Integration ที่ใช้ได้จริงชื่อ **`Codemagic Admin`** (ต้องตรงทุกตัวอักษร)
- ชื่อ `Life is` ในสโตร์ถูกใช้ไปแล้ว จึงใช้ `Life is: One-Sentence Diary`
  ชื่อบนหน้าจอมือถือยังเป็น `Life is` ตามเดิม ไม่ได้แก้ `CFBundleDisplayName`

### ✅ Life is ขึ้น TestFlight สำเร็จแล้ว — 27 ก.ค. 2026

เส้นทางนี้ **ผ่านจริงทั้งเส้น** ใช้ลอกได้เลยสำหรับโปรเจกต์ถัดไป

```yaml
integrations:
  app_store_connect: Codemagic Admin
environment:
  ios_signing:
    distribution_type: app_store
    bundle_identifier: com.lifeis.diary
```

- certificate: `Apple Distribution: Sutee Sodsai` — **ตัวเดิม ไม่ได้สร้างใหม่**
- profile: `Life is AppStore v1`
- ไม่มี certificate ของโปรเจกต์อื่นโดน revoke ระหว่างทาง

สิ่งที่ทำให้ผ่าน ไม่ใช่การแก้ signing แต่คือ **สร้าง App record ใน App Store
Connect ก่อน** แล้ว build ใหม่ — signing ถูกต้องมาตั้งแต่รอบก่อนหน้าแล้ว

## App Store Connect — ต้องทำก่อนสั่ง upload

My Apps → **New App**

| ช่อง | ใส่ |
|---|---|
| Platform | iOS |
| Name | ชื่อที่ไม่ซ้ำทั้งสโตร์ |
| Bundle ID | ตัวที่ลงทะเบียนไว้ใน Identifiers |
| SKU | `APPNAME-IOS-001` |
| User Access | Full Access |

API key ต้องมีสิทธิ์อย่างน้อย **App Manager** ไม่งั้น upload ไม่ผ่านแม้ IPA จะถูกต้อง

## ไฟล์อ้างอิงในเครื่อง

โปรเจกต์ที่ build ผ่านล่าสุด ใช้ลอก config ได้:

```
D:\AndroidStudioProjects\Tether Me\codemagic.yaml
D:\AndroidStudioProjects\carcarepro\codemagic.yaml
```
