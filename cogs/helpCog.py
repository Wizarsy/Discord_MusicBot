import discord
from discord.ext import commands

class Help_cog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command(name = "help", aliases = ["h"])
  async def Help(self, ctx):
    await ctx.send("""```teste```""")
    
async def setup(bot):
  await bot.add_cog(Help_cog(bot))