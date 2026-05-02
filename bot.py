import discord
import asyncio
import os
import random
import subprocess
from gtts import gTTS

# ตั้งค่า Intents
intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

client = discord.Client(intents=intents)

# หา path ของ ffmpeg อัตโนมัติ
def find_ffmpeg():
    # ลอง imageio-ffmpeg ก่อน
    try:
        import imageio_ffmpeg
        path = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"ใช้ ffmpeg จาก imageio: {path}")
        return path
    except Exception:
        pass
    # ลอง which
    result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)
    if result.stdout.strip():
        return result.stdout.strip()
    return 'ffmpeg'
FFMPEG_PATH = find_ffmpeg()

# ข้อความต้อนรับแบบสุ่ม
WELCOME_MESSAGES = [
    "{name} เข้ามาแล้ว",
    "ยินดีต้อนรับ {name}",
    "{name} มาถึงแล้ว",
    "สวัสดี {name}",
    "{name} เข้าร่วมห้องแล้ว",
]

# ข้อความตอนออก
LEAVE_MESSAGES = [
    "{name} ออกไปแล้ว",
    "{name} ลาก่อนนะ",
    "{name} ออกจากห้องแล้ว",
]

async def play_tts(voice_channel, text, lang='th'):
    """เชื่อมต่อ voice channel แล้วเล่นเสียง TTS"""
    guild = voice_channel.guild
    filename = f"tts_{guild.id}.mp3"

    try:
        # สร้างไฟล์เสียง
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)

        # เข้าห้องหรือย้ายไปห้องที่ถูกต้อง
        vc = guild.voice_client
        if vc and vc.is_connected():
            await vc.move_to(voice_channel)
        else:
            vc = await voice_channel.connect()

        # รอให้เสียงก่อนหน้าเล่นเสร็จก่อน
        while vc.is_playing():
            await asyncio.sleep(0.5)

        # เล่นเสียง
        vc.play(discord.FFmpegPCMAudio(filename, executable=FFMPEG_PATH))

        # รอให้เสียงเล่นเสร็จ
        while vc.is_playing():
            await asyncio.sleep(0.5)

        # ออกจาก voice channel
        await vc.disconnect()

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)


@client.event
async def on_ready():
    print(f"🔍 ffmpeg path: {FFMPEG_PATH}")
    print(f"✅ Bot พร้อมแล้ว: {client.user}")
    print(f"🌐 เชื่อมต่อ {len(client.guilds)} เซิร์ฟเวอร์")


@client.event
async def on_voice_state_update(member, before, after):
    # ข้ามถ้าเป็น Bot
    if member.bot:
        return

    name = member.display_name

    # คนเข้า Voice Channel
    if before.channel is None and after.channel is not None:
        text = random.choice(WELCOME_MESSAGES).format(name=name)
        print(f"📢 {text}")
        await play_tts(after.channel, text, lang='th')

    # คนออก Voice Channel
    elif before.channel is not None and after.channel is None:
        if len(before.channel.members) > 0:
            text = random.choice(LEAVE_MESSAGES).format(name=name)
            print(f"👋 {text}")
            await play_tts(before.channel, text, lang='th')

    # คนย้ายห้อง
    elif before.channel != after.channel and before.channel is not None and after.channel is not None:
        text = f"{name} ย้ายมาห้องนี้แล้ว"
        print(f"🔄 {text}")
        await play_tts(after.channel, text, lang='th')


# รัน Bot
TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    print("❌ ไม่พบ DISCORD_TOKEN! กรุณาตั้งค่า Environment Variable")
else:
    client.run(TOKEN)
