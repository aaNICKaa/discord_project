import discord
import asyncio
import os
import random
import subprocess
from gtts import gTTS

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

client = discord.Client(intents=intents)

def find_ffmpeg():
    try:
        import imageio_ffmpeg
        path = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"ใช้ ffmpeg จาก imageio: {path}")
        return path
    except Exception:
        pass
    result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)
    if result.stdout.strip():
        return result.stdout.strip()
    return 'ffmpeg'

FFMPEG_PATH = find_ffmpeg()

WELCOME_MESSAGES = [
    "{name} เข้ามาแล้ว",
    "ยินดีต้อนรับ {name}",
    "{name} มาถึงแล้ว",
    "สวัสดี {name}",
    "{name} เข้าร่วมห้องแล้ว",
]

LEAVE_MESSAGES = [
    "{name} ออกไปแล้ว",
    "{name} ลาก่อนนะ",
    "{name} ออกจากห้องแล้ว",
]

async def play_tts(voice_channel, text, lang='th'):
    guild = voice_channel.guild
    filename = f"tts_{guild.id}_{random.randint(1000,9999)}.mp3"

    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)

        vc = guild.voice_client
        if vc and vc.is_connected():
            await vc.move_to(voice_channel)
        else:
            vc = await voice_channel.connect()

        while vc.is_playing():
            await asyncio.sleep(0.3)

        finished = asyncio.Event()
        loop = asyncio.get_event_loop()

        def after(error):
            loop.call_soon_threadsafe(finished.set)

        vc.play(
            discord.FFmpegPCMAudio(filename, executable=FFMPEG_PATH, options='-vn'),
            after=after
        )

        await asyncio.wait_for(finished.wait(), timeout=30.0)
        await asyncio.sleep(0.3)
        await vc.disconnect()

    except asyncio.TimeoutError:
        print("Timeout: เล่นเสียงนานเกินไป")
        if guild.voice_client:
            await guild.voice_client.disconnect()
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        if guild.voice_client:
            await guild.voice_client.disconnect()
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
    if member.bot:
        return

    name = member.display_name

    if before.channel is None and after.channel is not None:
        text = random.choice(WELCOME_MESSAGES).format(name=name)
        print(f"📢 {text}")
        await play_tts(after.channel, text, lang='th')

    elif before.channel is not None and after.channel is None:
        if len(before.channel.members) > 0:
            text = random.choice(LEAVE_MESSAGES).format(name=name)
            print(f"👋 {text}")
            await play_tts(before.channel, text, lang='th')

    elif before.channel != after.channel and before.channel is not None and after.channel is not None:
        text = f"{name} ย้ายมาห้องนี้แล้ว"
        print(f"🔄 {text}")
        await play_tts(after.channel, text, lang='th')


TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    print("❌ ไม่พบ DISCORD_TOKEN!")
else:
    client.run(TOKEN)
