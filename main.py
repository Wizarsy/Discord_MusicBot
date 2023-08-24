import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix = ".", intents = discord.Intents.all(), help_command = None)

async def load():
  for cogs in os.listdir("./cogs"):
    if cogs.endswith('.py'):
      await bot.load_extension(f"cogs.{cogs[:-3]}")
  
async def main():
  await load()
  await bot.start(f"{os.getenv('TOKEN')}")
  
if __name__ == "__main__":
   asyncio.run(main())
  #  asyncio.run(load())
  #  bot.run(f"{os.getenv('TOKEN')}")