from yt_dlp import YoutubeDL


YDL_OP = {"format": "ba",
          "noplaylist": True,}
def ytSearch(music):
  with YoutubeDL(YDL_OP) as ydl:
    try:
      result = ydl.extract_info(f"ytsearch:{music}", download = False)["entries"][0]
    except:
      return False
  return result
  
  
  
# help(YoutubeDL)
print(ytSearch("https://youtu.be/lWA2pjMjpBs?si=GljeXBFr6xrH3EuY"))