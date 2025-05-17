import discord
from discord.ext import commands
from googletrans import Translator
import os

# Bot-Token und Channel-IDs aus Railway-Umgebungsvariablen
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_IDS = [
    int(os.getenv('TRANSLATE_CHANNEL_ID_1')),
    int(os.getenv('TRANSLATE_CHANNEL_ID_2')),
]

translator = Translator()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot ist online als {bot.user}')
    print(f'📢 Aktive Channels: {CHANNEL_IDS}')

    # Starte eine Begrüßung in beiden erlaubten Channels
    for channel_id in CHANNEL_IDS:
        channel = bot.get_channel(channel_id)
        if channel:
            try:
                await channel.send("✅ Übersetzungs-Bot ist bereit! (Englische Nachrichten werden automatisch ins Deutsche übersetzt.)")
            except Exception as e:
                print(f"❌ Fehler beim Senden in Channel {channel_id}: {e}")
        else:
            print(f"❌ Channel mit ID {channel_id} nicht gefunden.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id not in CHANNEL_IDS:
        return

    try:
        detected_lang = translator.detect(message.content).lang
        if detected_lang == 'en':
            translated = translator.translate(message.content, src='en', dest='de')
            await message.channel.send(f"Übersetzung: {translated.text}")
    except Exception as e:
        print(f"❌ Fehler bei der Übersetzung: {e}")

    await bot.process_commands(message)

bot.run(TOKEN)
