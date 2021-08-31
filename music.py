import discord
from discord.ext import commands
import youtube_dl
import urllib.request
import re
from requests import get
import json

class music(commands.Cog):
  
  def __init__ (self,client):
    self.client = client

  @commands.command()
  async def play(self,ctx,*url):
    
    if ctx.author.voice is None:
      await ctx.send("Join an audio channel first !")
      return

    voice_channel = ctx.author.voice.channel

    if ctx.voice_client is None:
      await voice_channel.connect()

    
    url = "+".join(url[:])
    if "http" not in url :
      search_keyword=url
      print (url)
      html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
      video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
      url = "https://www.youtube.com/watch?v=" + video_ids[0]

    ctx.voice_client.stop()
    FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options':'-vn'}

    YDL_OPTIONS = {'format':'bestaudio'}

    vc = ctx.voice_client
    msg = "```["+ctx.message.author.display_name+"] "+"Playing "
    
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl: 
      info = ydl.extract_info(url,download=False)
      
      sec = (info['duration'])%60
      min = int((info['duration'])/60)
      msg = msg + info['title'] +" Duration [" + str(min)+":"+str(sec)+"]" + '''
      ```'''+url
      await ctx.send(msg)

      url2 = info['formats'][0]['url']
      source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
      vc.play(source)
      

  @commands.command()
  async def hi(self,ctx):
    await ctx.send("Hello")

  @commands.command()
  async def join(self,ctx):
    if ctx.author.voice is None:
      await ctx.send("Join an audio channel first !")

    voice_channel = ctx.author.voice.channel

    if ctx.voice_client is None:
      await voice_channel.connect()

    else :
      await ctx.voice_client.move_to(voice_channel)

  
  @commands.command()
  async def leave(self,ctx):
    await ctx.voice_client.disconnect()
    await ctx.send("Disconnected !")
  @commands.command()
  async def reset(self,ctx):
    await ctx.invoke(self.client.get_command('leave'))
  @commands.command()
  async def stop(self,ctx):
    await ctx.invoke(self.client.get_command('pause'))

  @commands.command()
  async def pause(self,ctx):
    ctx.voice_client.pause()
    await ctx.send("Paused !")

  @commands.command()
  async def resume(self,ctx):
    ctx.voice_client.resume()
    await ctx.send("Resumed !")

  @commands.command()
  async def meme(self,ctx):
    content = get("https://meme-api.herokuapp.com/gimme").text
    data = json.loads(content,)
    meme = discord.Embed(title=f"{data['title']}", Color = discord.Color.random()).set_image(url=f"{data['url']}")
    await ctx.reply(embed=meme)

def setup(client):
  client.add_cog(music(client))
