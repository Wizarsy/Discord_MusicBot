import asyncio
import re

import discord
from discord.ext import commands
from yt_dlp import YoutubeDL

class music(commands.Cog):
  def __init__(self, bot):
    self.bot: commands.Bot = bot
    self.vc = None
    self.last_played = None
    self.queue = []
    self.emoji = {"ok": "✅",
                 "error": "❌",
                 "play": "▶️",
                 "pause": "⏸️",
                 "skip": "⏭️",
                 "clear": "💢",
                 "queue": "📋",
                 "dc": "⬇️"}
    self.YDL_OP = {"format": "ba",
                   "quiet": True}
    self.FFMPEG_OP = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                      "options": " -vn -sn"}
  
  @commands.Cog.listener()
  async def on_ready(self):
    await self.bot.tree.sync()
    print(f"Modulo {__name__} carregado.")
  
  async def ytSearch(self, ctx: commands.Context, query):
    with YoutubeDL(self.YDL_OP) as ydl:
      ydl.cache.remove()
      try:
        query = query if re.match(r"^(https|https://)?([A-Za-z0-9\-\_.]+\/)", query) else f"ytsearch:{query}"
        info  = await self.bot.loop.run_in_executor(None, lambda: ydl.extract_info(query, download = False))
        if "entries" in info:
          return [{"source": x["url"],
                   "title": x["title"],
                   "thumbnail": x["thumbnail"],
                   "request_by": ctx.author} for x in info["entries"]]
        else:
          return [{"source": info["url"],
                   "title": info["title"],
                   "thumbnail": info["thumbnail"],
                   "request_by": ctx.author}]
      except:
        return False
  
  async def join(self, user):
    if not self.vc:
        self.vc = await user.voice.channel.connect(timeout = 300.0)
    else:
      await self.vc.move_to(user.voice.channel)
      
  async def playMusic(self):
    if len(self.queue) > 0:
      await self.join(self.queue[0]["request_by"])
      url = self.queue[0]["source"]
      self.last_played = self.queue[0]
      self.queue.pop(0)
      self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OP), after = lambda e: print(e) if e else asyncio.run_coroutine_threadsafe(self.playMusic(), self.bot.loop))
       
  async def msg_embed(self, ctx: commands.Context, title = None, description = None, color = None, url = None):
    embed = discord.Embed(title = title, description = description, color = color)
    embed.set_author(name = ctx.author, icon_url = ctx.author.avatar)
    embed.set_thumbnail(url = url)
    await ctx.reply(embed = embed)
      
  @commands.hybrid_command(name = "play", aliases = ["p"], description = "Adiciona uma musica a lista, resume se estiver pausado ou toca se estiver parado")
  async def play(self, ctx: commands.Context, *, query = None):
    if not ctx.author.voice:
      await self.msg_embed(ctx, description = f"{self.emoji['error']} Entra em uma call o seu pau pequeno", color = discord.Colour.red())
    else:
      if not self.vc:
        await self.join(ctx.author)
      if not query:
        if self.vc.is_paused():
          if not ctx.interaction:
            await ctx.message.add_reaction("▶️")
          await self.msg_embed(ctx, description = f"{self.emoji['play']} Tocando - {self.last_played['title']}", url = self.last_played['thumbnail'], color = discord.Colour.blue())
          self.vc.resume()
        elif len(self.queue) and not self.vc.is_playing():
          if not ctx.interaction:
            await ctx.message.add_reaction("▶️")
          await self.msg_embed(ctx, description = f"{self.emoji['play']} Tocando...", color = discord.Colour.blue())
          await self.playMusic()
        elif self.vc.is_playing():
          await self.msg_embed(ctx, description = f"{self.emoji['play']} Já está tocando", color = discord.Colour.light_grey())
        else:
          await self.msg_embed(ctx, description = f"{self.emoji['queue']} Fila Vazia", color = discord.Colour.light_grey())
      else:
        if not ctx.interaction:
          await ctx.message.add_reaction("✅")
        await self.msg_embed(ctx, description = f"{self.emoji['ok']} Adicionado a fila", color = discord.Colour.green())
        song = await self.ytSearch(ctx, query)
        if not song:
          if not ctx.interaction:
            await ctx.message.clear_reaction("✅")
            await ctx.message.add_reaction("❌")
          await self.msg_embed(ctx, description = f"{self.emoji['error']} Achei porra nenhuma bixo", color = discord.Colour.red())
        else:
          self.queue.extend(song)
          if not self.vc.is_playing():
            await self.playMusic()
                
  @commands.hybrid_command(name = "pause", description = "Pausa de tocar a musica atual")
  async def pause(self, ctx: commands.Context):
    if self.vc:
      if not ctx.interaction:
        await ctx.message.add_reaction("⏸️")
      await self.msg_embed(ctx, description = f"{self.emoji['pause']} Pausado...", color = discord.Colour.blue())
      self.vc.pause()
  
  @commands.hybrid_command(name = "resume", aliases = ["r"], description = "Retoma a musica atual")
  async def resume(self, ctx: commands.Context):
    if self.vc:
      if not ctx.interaction:
        await ctx.message.add_reaction("▶️")
      await self.msg_embed(ctx, description = f"{self.emoji['play']} Tocando - {self.last_played['title']}", url = self.last_played['thumbnail'], color = discord.Colour.blue())
      self.vc.resume()
  
  @commands.hybrid_command(name = "skip", aliases = ["sp"], description = "Pula a musica atual")
  async def skip(self, ctx: commands.Context):
    if self.vc and len(self.queue) > 0:
      if not ctx.interaction:
        await ctx.message.add_reaction("⏭️")
      await self.msg_embed(ctx, description = f"{self.emoji['skip']} Pulando...", color = discord.Colour.blue())
      self.vc.stop()
    else:
      await self.msg_embed(ctx, description = f"{self.emoji['queue']} Fila Vazia", color = discord.Colour.light_grey())
  
  @commands.hybrid_command(name = "queue", aliases = ["q"], description = "Mostra a fila de musicas")
  async def queue(self, ctx: commands.Context):
    if len(self.queue) > 0:
      if not ctx.interaction:
        await ctx.message.add_reaction("📋")
      queue_song = [discord.Embed(description = f"{self.emoji['queue']} Fila", color = discord.Colour.red())]
      for i in range(len(self.queue)):
        if i > 5:
          break
        embed = discord.Embed(title = f"{i + 1}: {self.queue[i]['title']}", color = discord.Colour.red())
        embed.set_author(name = self.queue[i]["request_by"], icon_url = self.queue[0]["request_by"].avatar)
        embed.set_thumbnail(url = self.queue[i]["thumbnail"])
        queue_song.append(embed)
      await ctx.reply(embeds = queue_song)
    else:
      await self.msg_embed(ctx, description = f"{self.emoji['queue']} Fila vazia", color = discord.Colour.light_grey())
  
  @commands.hybrid_command(name = "clear", aliases = ["c"], description = "Limpa a fila de musicas e para a atual")
  async def clear(self, ctx: commands.Context):
    if self.vc and (len(self.queue) > 0 or self.is_playing()):
      if not ctx.interaction:
        await ctx.message.add_reaction("💢")
      await self.msg_embed(ctx, description = f"{self.emoji['clear']} Fila limpa", color = discord.Colour.red())
      self.queue = []
      self.vc.stop()
    else:
      await self.msg_embed(ctx, description = f"{self.emoji['queue']} Fila vazia ou fora da call", color = discord.Colour.light_grey())
  
  @commands.hybrid_command(name = "disconnect", aliases = ["dc"], description = "Desconecta o bot da call")
  async def disconnect(self, ctx: commands.Context):
    if self.vc:
      if not ctx.interaction:
        await ctx.message.add_reaction("⬇️")
      await self.msg_embed(ctx, description = f"{self.emoji['dc']} Desconectando", color = discord.Colour.blue())
      self.queue = []
      await self.vc.disconnect()
      
  @commands.hybrid_command(name = "delete", aliases = ["del"], description = "Apaga uma musica da fila")
  async def delete(self, ctx: commands.Context, *, index: int):
    if self.vc and len(self.queue) > 0:
      try:
        self.queue.pop(index - 1)
      except:
        await self.msg_embed(ctx, description = f"{self.emoji['error']} Erro", color = discord.Colour.red())
    else:
      await self.msg_embed(ctx, description = f"{self.emoji['queue']} Fila vazia ou fora da call", color = discord.Colour.light_grey())

async def setup(bot: commands.Bot):
  await bot.add_cog(music(bot))