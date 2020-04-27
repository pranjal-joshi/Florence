
import pafy
import vlc
import urllib.parse, urllib.request
import re
from globalVariables import *

class florenceMultimedia:

    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def youtubeSearch(self,query):
        try:
            query = removeStreamingWords(query)
            q = urllib.parse.urlencode({"search_query":query})
            url = "http://www.youtube.com/results?"+q
            if DEBUG:
                print("[+] YouTube Search URL: %s" % url)
            html = urllib.request.urlopen(url)
            search = re.findall(r'href=\"\/watch\?v=(.{11})', html.read().decode())
            return ("http://www.youtube.com/watch?v=" + search[0]),True
        except Exception as e:
            return str(e), False

    def youtubeStreamAudio(self,url):
        try:
            video = pafy.new(url)
            audio = video.getbestaudio()
            self.media = self.instance.media_new(audio.url)
            self.player.set_media(self.media)
            self.player.play()
            return None, True
        except Exception as e:
            return str(e), False

    def youtubeStreamControl(self,action):
        if action == 'toggle':
            self.player.pause()
        elif action == 'stop':
            self.player.stop()
