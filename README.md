# 🎙️ Discord TTS Bot - อ่านชื่อเวลาคนเข้าห้อง

Bot อ่านชื่อสมาชิกเวลาเข้า/ออก/ย้าย Voice Channel ด้วยเสียงภาษาไทย

---

## ✅ ฟีเจอร์
- 📢 ประกาศเมื่อคนเข้าห้อง (ภาษาไทย)
- 👋 ประกาศเมื่อคนออกห้อง
- 🔄 ประกาศเมื่อคนย้ายห้อง
- 🎲 ข้อความสุ่มหลายแบบ ไม่ซ้ำจำเจ
- 🤖 ข้ามประกาศ Bot อื่น

---

## 🚀 วิธีติดตั้ง (ฟรี ด้วย Railway)

### ขั้นตอนที่ 1 - สร้าง Discord Bot

1. ไปที่ https://discord.com/developers/applications
2. กด **"New Application"** ตั้งชื่อ Bot
3. ไปที่แถบ **"Bot"** → กด **"Add Bot"**
4. เปิด **Privileged Gateway Intents** ทั้ง 3 ตัว:
   - ✅ PRESENCE INTENT
   - ✅ SERVER MEMBERS INTENT
   - ✅ MESSAGE CONTENT INTENT
5. คัดลอก **Token** เก็บไว้ (กด Reset Token ถ้าไม่เห็น)

### ขั้นตอนที่ 2 - เชิญ Bot เข้า Server

1. ไปที่แถบ **"OAuth2"** → **"URL Generator"**
2. เลือก Scopes: ✅ `bot`
3. เลือก Bot Permissions:
   - ✅ Connect
   - ✅ Speak
   - ✅ Use Voice Activity
4. คัดลอก URL → เปิดในเบราว์เซอร์ → เลือก Server → Authorize

### ขั้นตอนที่ 3 - Deploy บน Railway (ฟรี)

1. สมัคร/Login ที่ https://railway.app (ใช้ GitHub login)
2. กด **"New Project"** → **"Deploy from GitHub repo"**
3. อัปโหลดโฟลเดอร์นี้ไปที่ GitHub ก่อน หรือใช้ **"Empty Project"** แล้ว drag & drop ไฟล์
4. ไปที่ **Variables** → เพิ่ม:
   ```
   DISCORD_TOKEN = your_bot_token_here
   ```
5. กด **Deploy** → รอสักครู่ → Bot ออนไลน์! 🎉

---

## 🧪 ทดสอบบนเครื่องตัวเอง

```bash
# 1. ติดตั้ง dependencies
pip install -r requirements.txt

# 2. ติดตั้ง ffmpeg
# Mac:     brew install ffmpeg
# Ubuntu:  sudo apt install ffmpeg
# Windows: https://ffmpeg.org/download.html

# 3. ตั้งค่า Token
export DISCORD_TOKEN="your_token_here"   # Mac/Linux
set DISCORD_TOKEN=your_token_here        # Windows

# 4. รัน
python bot.py
```

---

## ✏️ ปรับแต่งข้อความ

แก้ไขในไฟล์ `bot.py` ส่วน `WELCOME_MESSAGES` และ `LEAVE_MESSAGES`:

```python
WELCOME_MESSAGES = [
    "{name} เข้ามาแล้ว",
    "ยินดีต้อนรับ {name}",
    # เพิ่มข้อความตามชอบ...
]
```

---

## 📁 โครงสร้างไฟล์

```
discord-tts-bot/
├── bot.py              # โค้ดหลัก
├── requirements.txt    # Python packages
├── Procfile            # คำสั่ง start สำหรับ Railway
├── nixpacks.toml       # ติดตั้ง ffmpeg อัตโนมัติบน Railway
└── README.md           # คู่มือนี้
```
