import os
import discord
from discord.ext import commands
from google.generativeai import configure, GenerativeModel
from dotenv import load_dotenv

# Zmienne z .env będą w HOSTingu, nie w repo
load_dotenv()
print("TOKEN z .env:", os.getenv('DISCORD_TOKEN')[:10])

configure(api_key=os.getenv('GEMINI_API_KEY'))
model = GenerativeModel('gemini-1.5-flash')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='vs')
async def vs(ctx, champion: str):
    await ctx.send(f'🔍 Szukam matchupu Vayne vs **{champion}**...')
    prompt = f"""
Jesteś ekspertem League of Legends. Opisz po polsku krótko i konkretnie:
1) Główne skille {champion} które są groźne dla Vayne na topie
2) Jak grać ten matchup jako Vayne (czasy walki, minimap, wave, shovać itd.)
3) Wskazówki: itemizacja, timing, cheese
Nie przesadzaj, odpowiedź w 5–7 zdań.
"""
    try:
        response = model.generate_content(prompt)
        await ctx.send(response.text)
    except Exception as e:
        await ctx.send(f'❌ Błąd: `{e}`')
        print(e)

@bot.event
async def on_ready():
    print(f'Bot działa jako {bot.user}')

@bot.command(name='joint')
async def joint(ctx):
    await ctx.send('✅ Zapisano jointa (mock)!')

bot.run(os.getenv('DISCORD_TOKEN'))
