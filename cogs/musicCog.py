import asyncio
from audioop import add
from email import message
import discord
from discord.ext import commands
from yt_dlp import YoutubeDL

class Music(commands.Cog):
  def __init__(self, bot):
    self.bot: commands.Bot = bot
    self.vc = None
    self.is_playing = False
    self.is_paused = False
    self.last_played = None
    self.queue = []
    self.YDL_OP = {"format": "ba",
                   "noplaylist": True,
                   "quiet": True}
    self.FFMPEG_OP = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                      "options": " -vn -sn"}
  
  @commands.Cog.listener()
  async def on_ready(self):
    await self.bot.tree.sync()
    print(f"\33[32mModulo {__name__} carregado.\33[0m")
    
  def ytSearch(self, music):
    with YoutubeDL(self.YDL_OP) as ydl:
      try:
        result = ydl.extract_info(f"ytsearch:{music}", download = False)["entries"][0]
      except:
        return False
    return {"source": result["url"],
            "title": result["title"]}
    
  async def playMusic(self):
    if len(self.queue) > 0 and self.is_playing:
      if self.vc == None:
        self.vc = await self.queue[0][1].connect(timeout = 300)
      else:
        await self.vc.move_to(self.queue[0][1])
      url = self.queue[0][0]["source"]
      self.queue.pop(0)
      self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OP), after = lambda a: asyncio.run_coroutine_threadsafe(self.playMusic(), self.bot.loop))
    else:
      self.is_playing = False
      self.is_paused = False
  
  @commands.hybrid_command(name = "play", aliases = ["p"], description = "Adiciona uma musica a lista, resume se estiver pausado ou toca se estiver parado")
  async def Play(self, ctx: commands.Context, *, query = ""):
    if ctx.author.voice is None:
      await ctx.reply("```Entra em uma call o seu pau pequeno```")
    elif len(query) == 0:
      if self.is_paused:
        if not ctx.interaction:
          await ctx.message.add_reaction("▶️")
        else:
          await ctx.send("▶️")
        self.is_playing = True
        self.vc.resume()
      elif len(self.queue) > 0 and not self.is_playing:
        self.is_playing = True
        await self.playMusic()
      else:
        await ctx.send("```Fila Vazia```")
    else:
      if not ctx.interaction:
        await ctx.message.add_reaction("✅")
      else:
        await ctx.send("✅")
      song = self.ytSearch(query)
      if not song:
        if not ctx.interaction:
          await ctx.message.clear_reaction("✅")
          await ctx.message.add_reaction("❌")
        else:
          await ctx.send("❌")
        await ctx.reply("```Achei porra nenhuma bixo```")
      else:
        user = ctx.author
        vc = user.voice.channel
        self.queue.append([song, vc, user])
        if len(self.queue) > 0 and (not self.is_playing and not self.is_paused):
          self.is_playing = True
          await self.playMusic() 
                
  @commands.hybrid_command(name = "pause", description = "Pausa de tocar a musica atual")
  async def Pause(self, ctx: commands.Context):
    if self.vc != None:
      if not ctx.interaction:
        await ctx.message.add_reaction("⏸️")
      else:
        await ctx.send("⏸️")
      self.is_playing = False
      self.is_paused = True
      self.vc.pause()
  
  @commands.hybrid_command(name = "resume", aliases = ["r"], description = "Retoma a musica atual")
  async def Resume(self, ctx: commands.Context):
    if self.vc != None:
      if not ctx.interaction:
        await ctx.message.add_reaction("▶️")
      else:
        await ctx.send("▶️")
      self.is_paused = False
      self.is_playing = True
      self.vc.resume()
  
  @commands.hybrid_command(name = "skip", aliases = ["sp"], description = "Pula a musica atual")
  async def Skip(self, ctx: commands.Context):
    if self.vc != None and len(self.queue) > 0:
      if not ctx.interaction:
        await ctx.message.add_reaction("⏭️")
      else:
        await ctx.send("⏭️")
      self.vc.stop()
    else:
      await ctx.send("```Fila Vazia```")
      
  @commands.hybrid_command(name = "stop", aliases = ["s"], description = "Para de tocar musica")
  async def Stop(self, ctx: commands.Context):
    if self.vc != None:
      if not ctx.interaction:
        await ctx.message.add_reaction("🛑")
      else:
        await ctx.send("🛑")
      self.is_playing = False
      self.is_paused = False    
      self.vc.stop()
  
  @commands.hybrid_command(name = "queue", aliases = ["q"], description = "Mostra a fila de musicas")
  async def Queue(self, ctx: commands.Context):
    if len(self.queue) > 0:
      if not ctx.interaction:
        await ctx.message.add_reaction("📋")
      queue_song = ''
      for song in self.queue:
        queue_song += f"{song[0]['title']} ----- Pedido por: {song[2]}\n"
      await ctx.send(f"```{queue_song}```")
    else:
      await ctx.send("```Fila Vazia```")
  
  @commands.hybrid_command(name = "clear", aliases = ["c"], description = "Limpa a fila de musicas e para a atual")
  async def Clear(self, ctx: commands.Context):
    if self.vc != None:
      if not ctx.interaction:
        await ctx.message.add_reaction("💢")
      else:
        await ctx.send("💢")
      self.is_playing = False
      self.is_paused = False 
      self.queue = []
      self.vc.stop()
  
  @commands.hybrid_command(name = "disconnect", aliases = ["dc"], description = "Desconecta o bot da call")
  async def Disconnect(self, ctx: commands.Context):
    if self.vc != None:
      if not ctx.interaction:
        await ctx.message.add_reaction("⬇️")
      else:
        await ctx.send("⬇️")
      self.is_playing = False
      self.is_paused = False 
      self.queue = []
      self.vc.stop()
      await self.vc.disconnect()

async def setup(bot: commands.Bot):
  await bot.add_cog(Music(bot))