from pickle import FALSE
import discord
from discord.ext import commands

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot: commands.Bot = bot
    
  @commands.Cog.listener()
  async def on_ready(self):
    await self.bot.tree.sync()
    print(f"Modulo {__name__} carregado.")
    
  @commands.hybrid_command(name = "help", aliases = ["h"], description = "Mostra os comandos disponiveis")
  async def Help(self, ctx: commands.Context):
    if not ctx.interaction:
      await ctx.message.add_reaction("📖")
    embed = discord.Embed(description = f"📖 Comandos disponiveis:", color = discord.Colour.gold())
    embed.set_author(name = ctx.author, icon_url = ctx.author.avatar)
    embed.set_thumbnail(url = ctx.author.avatar)
    embed.add_field(name = "/play .play .p", value = "Adiciona uma musica a lista, resume se estiver pausado ou toca se estiver parado", inline = False)
    embed.add_field(name = "/pause .pause", value = "Pausa de tocar a musica atual", inline = False)
    embed.add_field(name = "/resume .resume .r", value = "Retoma a musica atual", inline = False)
    embed.add_field(name = "/skip .skip .sp", value = "Pula a musica atual", inline = False)
    embed.add_field(name = "/queue .queue .q", value = "Mostra a fila de musicas", inline = False)
    embed.add_field(name = "/clear .clear .c", value = "Limpa a fila de musicas e para a atual", inline = False)
    embed.add_field(name = "/disconnect .disconnect .dc", value = "Desconecta o bot da call", inline = False)
    embed.add_field(name = "/delete .delete .del", value = "Apaga uma musica da fila", inline = False)
    await ctx.send(embed = embed)
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Help(bot))