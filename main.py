import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix = ".", intents = discord.Intents.all(), help_command = None, activity = discord.Game(name='.help | /help'))

@bot.event
async def on_ready():
  print("\33[32mBot esta online e conectado ao discord\33[0m")
  
async def load():
  for cogs in os.listdir("./cogs"):
    if cogs.endswith('.py'):
      await bot.load_extension(f"cogs.{cogs[:-3]}")
  
async def main():
  await load()
  await bot.start(os.getenv('TOKEN'))
  
if __name__ == "__main__":
  if os.getenv('ENV') == "DEV":
    bot.run(os.getenv('TOKEN'))
    asyncio.run(load())
  else:
    asyncio.run(main())