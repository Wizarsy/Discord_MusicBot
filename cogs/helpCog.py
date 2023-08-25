import discord
from discord.ext import commands

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot: commands.Bot = bot
    
  @commands.Cog.listener()
  async def on_ready(self):
    await self.bot.tree.sync()
    print(f"\33[32mModulo {__name__} carregado.\33[0m")
    
  @commands.hybrid_command(name = "help", aliases = ["h"], description = "Mostra os comandos disponiveis")
  async def Help(self, ctx: commands.Context):
    if not ctx.interaction:
      await ctx.message.add_reaction("📖")
    await ctx.send("""
```Comandos disponiveis:

/play .play .p - Adiciona uma musica a lista, resume se estiver pausado ou toca se estiver parado
/pause .pause - Pausa de tocar a musica atual
/resume .resume .r - Retoma a musica atual
/skip .skip .sp - Pula a musica atual
/stop .stop - Para de tocar musica
/queue .queue .q - Mostra a fila de musicas
/clear .clear .c - Limpa a fila de musicas e para a atual
/disconnect .disconnect .dc - Desconecta o bot da call
```
""")
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Help(bot))