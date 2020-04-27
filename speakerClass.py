
from globalVariables import *
import pyttsx3
import threading

class florenceTalks:

    def __init__(self, gender='female', rate=190):
        voice_list = []
        if gender == 'female':
            self.voice_id_index = 1
        else:
            self.voice_id_index = 0
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        for v in self.voices:
            voice_list.append(v.id)
        self.engine.setProperty('voice',voice_list[self.voice_id_index])
        self.engine.setProperty('rate',rate)
        if DEBUG:
            print("[+] Initializing florenceTalks class..")
            print("[+] Voice: %s" % voice_list[self.voice_id_index])
    
    def setSpeechRate(self, rate=190):
        self.engine.setProperty('rate',rate)

    def talk(self, text='Hello world'):
        if DEBUG:
            print("[+] TTS Text: %s" % text)
        self.engine.say(text)
        self.engine.runAndWait()

    def talkInBackground(self,text):
        threading.Thread(target=self.talk,args=(text,)).start()

    def goodbye(self):
        self.engine.stop()
            