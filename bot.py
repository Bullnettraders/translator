import discord
from discord.ext import commands
from googletrans import Translator
import os

# Token aus Railway
TOKEN = os.getenv('DISCORD_TOKEN')

# Channel-IDs als Umgebungsvariablen lesen
channel_id_1 = os.getenv('TRANSLATE_CHANNEL_ID_1')
channel_id_2 = os.getenv('TRANSLATE_CHANNEL_ID_2')

# Fehlerprüfung: Wurden die Channel-IDs gesetzt?
if not channel_id_1 or not channel_id_2:
    raise ValueError("❌ Umgebungsvariablen TRANSLATE_CHANNEL_ID_1 und/oder TRANSLATE_CHANNEL_ID_2 fehlen!")

# Channel-IDs als int speichern
CHANNEL_IDS = [int(channel_id_1), int(channel_id_2)]

# Übersetzer
translator = Translator()

# Bot-Initialisierung mit Intent für Nachrichteninhalt
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot ist online als {bot.user}')
    print(f'📢 Aktive Übersetzungs-Channels: {CHANNEL_IDS}')

    # Begrüßung in erlaubten Channels
    for channel_id in CHANNEL_IDS:
        channel = bot.get_channel(channel_id)
        if channel:
            try:
                await channel.send("✅ Übersetzungs-Bot ist bereit! Englische Nachrichten werden automatisch ins Deutsche übersetzt.")
            except Exception as e:
                print(f"❌ Fehler beim Senden in Channel {channel_id}: {e}")
        else:
            print(f"❌ Channel mit ID {channel_id} nicht gefunden (Bot hat vielleicht keine Rechte?).")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Nur Nachrichten aus erlaubten Channels übersetzen
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
