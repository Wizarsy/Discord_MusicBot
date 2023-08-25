import discord
from discord.ext import commands

class Help_cog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command(name = "help", aliases = ["h"])
  async def Help(self, ctx):
    await ctx.message.add_reaction("📖")
    await ctx.send("""
```Comandos disponiveis:

.play .p - Adiciona uma musica a lista, resume se estiver pausado ou toca se estiver parado
.stop - Para de tocar musica
.pause - Pausa de tocar a musica atual
.resume .r - Resume a musica atual
.skip .sp - Pula a musica atual
.queue .q - Mostra a fila de musicas
.clear .c - Limpa a fila de musicas e para a atual
.disconnect .dc - Desconecta o bot da call
```
""")
    
async def setup(bot):
  await bot.add_cog(Help_cog(bot))