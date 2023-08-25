import asyncio
from audioop import add
from email import message
import discord
from discord.ext import commands
from yt_dlp import YoutubeDL

class Music_cog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
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
  
  def ytSearch(self, music):
    with YoutubeDL(self.YDL_OP) as ydl:
      try:
        result = ydl.extract_info(f"ytsearch:{music}", download = False)["entries"][0]
      except:
        return False
    return {"source": result["url"],
            "title": result["title"]}
    
  async def playMusic(self, ctx):
    if len(self.queue) > 0 and self.is_playing:
      if self.vc == None:
        self.vc = await self.queue[0][1].connect(timeout = 300)
      else:
        await self.vc.move_to(self.queue[0][1])
      url = self.queue[0][0]["source"]
      self.queue.pop(0)
      self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OP), after = lambda a: asyncio.run_coroutine_threadsafe(self.playMusic(ctx), self.bot.loop))
    else:
      self.is_playing = False
  
  @commands.command(name = "play", aliases =["p"])
  async def Play(self, ctx, *args):
    if ctx.author.voice is None:
      await ctx.reply("```Entra em uma call o seu pau pequeno```")
    elif len(args) == 0:
      if self.is_paused:
        await ctx.message.add_reaction("▶️")
        self.is_playing = True
        self.vc.resume()
      elif len(self.queue) > 0 and self.is_playing == False:
        self.is_playing = True
        await self.playMusic(ctx)
      else:
        await ctx.send("```Fila Vazia```")
    else:
      await ctx.message.add_reaction("✅")
      search = " ".join(args)
      song = self.ytSearch(search)
      if song == False:
        await ctx.message.clear_reaction("✅")
        await ctx.message.add_reaction("❌")
        await ctx.reply("```Achei porra nenhuma bixo```")
      else:
        user = ctx.author
        vc = user.voice.channel
        self.queue.append([song, vc, user])
        if self.is_playing == False:
          self.is_playing = True
          await self.playMusic(ctx) 
                
  @commands.command(name = "pause")
  async def Pause(self, ctx):
    if self.vc != None:
      await ctx.message.add_reaction("⏸️")
      self.is_playing = False
      self.is_paused = True
      self.vc.pause()
  
  @commands.command(name = "resume", aliases = ["r"])
  async def Resume(self, ctx):
    if self.vc != None:
      await ctx.message.add_reaction("▶️")
      self.is_paused = False
      self.is_playing = True
      self.vc.resume()
  
  @commands.command(name = "skip", aliases = ["sp"])
  async def Skip(self, ctx):
    if self.vc != None and len(self.queue) > 0:
      await ctx.message.add_reaction("⏭️")
      self.vc.stop()
    else:
      await ctx.send("```Fila Vazia```")
      
  @commands.command(name = "stop", aliases = ["s"])
  async def Stop(self, ctx):
    if self.vc != None:
      await ctx.message.add_reaction("🛑")
      self.is_playing = False
      self.is_paused = False    
      self.vc.stop()
  
  @commands.command(name = "queue", aliases = ["q"])
  async def Queue(self, ctx):
    if len(self.queue) > 0:
      await ctx.message.add_reaction("📋")
      queue_song = ''
      for song in self.queue:
        queue_song += f"{song[0]['title']} ----- Pedido por: {song[2]}\n"
      await ctx.send(f"```{queue_song}```")
    else:
      await ctx.send("```Fila Vazia```")
  
  @commands.command(name = "clear", aliases = ["c"])
  async def Clear(self, ctx):
    if self.vc != None:
      await ctx.message.add_reaction("💢")
      self.is_playing = False
      self.is_paused = False 
      self.queue = []
      self.vc.stop()
  
  @commands.command(name = "disconnect", aliases = ["dc"])
  async def Disconnect(self, ctx):
    if self.vc != None:
      await ctx.message.add_reaction("📞")
      self.is_playing = False
      self.is_paused = False 
      self.queue = []
      self.vc.stop()
      await self.vc.disconnect()

async def setup(bot):
  await bot.add_cog(Music_cog(bot))