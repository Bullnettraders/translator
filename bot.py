import discord
from discord.ext import commands
from googletrans import Translator
import os

# Token und Channel-ID aus Umgebungsvariablen
TOKEN = os.getenv('DISCORD_TOKEN')
ALLOWED_CHANNEL_ID = int(os.getenv('TRANSLATE_CHANNEL_ID'))

translator = Translator()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot ist online als {bot.user}')
    print(f'Aktiver Channel: {ALLOWED_CHANNEL_ID}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Nur in dem erlaubten Channel übersetzen
    if message.channel.id != ALLOWED_CHANNEL_ID:
        return

    try:
        detected_lang = translator.detect(message.content).lang
        if detected_lang == 'en':
            translated = translator.translate(message.content, src='en', dest='de')
            await message.channel.send(f"Übersetzung: {translated.text}")
    except Exception as e:
        print(f"Fehler bei der Übersetzung: {e}")

    await bot.process_commands(message)

bot.run(TOKEN)
