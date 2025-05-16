import discord
from discord.ext import commands
from googletrans import Translator
import os

# Bot-Token aus Umgebungsvariablen lesen
TOKEN = os.getenv('DISCORD_TOKEN')

# Translator initialisieren
translator = Translator()

# Bot definieren
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot ist online als {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
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
