import asyncio
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
                   "noplaylist": True,}
    
    self.FFMPEG_OP = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                      "options": " -vn"}
  
  def ytSearch(self, music):
    with YoutubeDL(self.YDL_OP) as ydl:
      try:
        result = ydl.extract_info(f"ytsearch:{music}", download = False)["entries"][0]
      except:
        return False
    return {"source": result["url"],
            "title": result["title"]}
    
  async def playMusic(self, ctx):
    if len(self.queue) > 0:
      self.is_playing = True
      await ctx.send(f'ok {self.is_playing}')
      if self.vc == None:
        self.vc = await self.queue[0][1].connect()
      else:
        await self.vc.move_to(self.queue[0][1])
      url = self.queue[0][0]["source"]
      self.queue.pop(0)
      await self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OP), after = asyncio.run_coroutine_threadsafe(lambda: self.playMusic(), self.bot.loop))
    else:
      self.is_playing = False
  
  @commands.command(name = "play", aliases =["p"])
  async def Play(self, ctx, *args):
    if ctx.author.voice is None:
      await ctx.reply("Entra em uma call o seu pau pequeno")
    elif self.is_paused:
      self.vc.resume()
    else:
      search = " ".join(args)
      song = self.ytSearch(search)
      if song == False:
        await ctx.reply("Achei porra nenhuma bixo")
      else:
        user = ctx.author
        vc = user.voice.channel
        self.queue.append([song, vc, user])
        if self.is_playing == False:
            await self.playMusic(ctx) 
        else:
          self.is_playing = False
                
  @commands.command(name = "pause")
  async def Pause(self, ctx):
    if self.is_playing:
      self.vc.pause()
      self.is_playing = False
      self.is_paused = True
  
  @commands.command(name = "resume", aliases = ["r"])
  async def Resume(self, ctx):
    if self.is_paused:
      self.vc.resume()
      self.is_playing = True
      self.is_paused = False
  
  @commands.command(name = "skip", aliases = ["sp"])
  async def Skip(self, ctx):
    if self.is_playing:
      self.vc.stop()
      await self.playMusic()
      
  @commands.command(name = "stop", aliases = ["s"])
  async def Stop(self, ctx):
    print(self.is_playing)
    if self.is_playing:
      self.vc.stop()
      self.is_playing = False
      self.is_paused = False    
  
  @commands.command(name = "queue", aliases = ["q"])
  async def Queue(self, ctx):
    if len(self.queue) > 0:
      for song in self.queue:
        queue += f"{song[0]['title']}\n"
      await ctx.send(queue)    
  
  @commands.command(name = "clear", aliases = ["c"])
  async def Clear(self, ctx):
    if self.is_playing:
      self.vc.stop()
      self.queue = []
      self.is_playing = False
      self.is_paused = False 

async def setup(bot):
  await bot.add_cog(Music_cog(bot))