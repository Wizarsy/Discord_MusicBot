from yt_dlp import YoutubeDL


YDL_OP = {"format": "ba",
          "noplaylist": True,}
def ytSearch(music):
  with YoutubeDL(YDL_OP) as ydl:
    try:
      result = ydl.extract_info(f"ytsearch:{music}", download = False)["entries"][0]
    except:
      return False
  return result['url']
  
  
  
# help(YoutubeDL)
print(ytSearch("https://youtu.be/ia1iuXbEaYQ?si=1CmoY39PHxCAYz9S"))