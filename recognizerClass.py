
from globalVariables import *
import speech_recognition as sr
import sys

#'Florence-5acbc25bc627.json'

class florenceListens:

    def __init__(self,CredFilePath):

        if DEBUG:
            print("[+] Initializing florenceListens class...")
        try:
            credFile = open(CredFilePath)
            self.credData = credFile.read()
            credFile.close()
        except:
            print("[Error] Could not access the credential file. Check it's path!")
            sys.exit(1)

        self.r = sr.Recognizer()
        if DEBUG:
            print("[+] Available Audio Sources: " + str(sr.Microphone().list_microphone_names()))
        with sr.Microphone() as source:
            print("[+] Analyzing & Calibrating ambient noise levels..")
            self.r.adjust_for_ambient_noise(source)
            self.r.pause_threshold = 1

    def listen(self,recalibrate=True,CalibrateDuration=1):
        playStartSpeakingSound()
        with sr.Microphone() as source:
            if recalibrate:
                print("[+] Analyzing & Calibrating ambient noise levels..")
                self.r.adjust_for_ambient_noise(source,duration=CalibrateDuration)
            print("[+] Listening...")
            self.audio = self.r.listen(source)
    
    def recognize(self,language="en-IN"):
        success = True
        try:
            self.out = self.r.recognize_google_cloud(self.audio, credentials_json=self.credData, language=language).strip()
        except sr.RequestError:
            print("[Error] RequestError: API Unavailable/Unreachble. Check Connectivity/Credentials!")
            self.out = "Speech API is not available at this time."
            success = False
        except sr.UnknownValueError:
            print("[Error] UnknownValueError: API could not recognize the audio!")
            self.out = getUnknownValueErrorPhrase()
            success = False
        except Exception as e:
            print("[Error] Unknown exception: %s" % e)
            self.out = "Unknown Exception Occured: %s" % e
            success = False
        if DEBUG:
            print("[+] STT Output: %s" % self.out)
        return self.out, success

    def listenAndRecognize(self,recalibrate=True,CalibrateDuration=1,language="en-IN"):
        self.listen(recalibrate=recalibrate,CalibrateDuration=CalibrateDuration)
        return self.recognize(language=language)
    
