
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
            print("[+] Available Audio Sources:")
            for mics in sr.Microphone().list_microphone_names():
                print("[>] %s" % str(mics).replace("\n",''))
        with sr.Microphone() as source:
            self.r.pause_threshold = PAUSE_THRESH
            # tune this params for better mic performance
            self.r.dynamic_energy_adjustment_damping = DAMPING_RATIO
            self.r.dynamic_energy_ratio = ENERGY_RATIO

    def listen(self,recalibrate=True,CalibrateDuration=CAL_DURATION,startSpeakingSound=EN_START_SPEAKING_SOUND,timeout=None):
        if startSpeakingSound:
            playStartSpeakingSound()
        with sr.Microphone() as source:
            if recalibrate:
                print("[+] Analyzing & Calibrating ambient noise levels..")
                self.r.adjust_for_ambient_noise(source,duration=CalibrateDuration)
            print("[+] Listening...")
            try:
                self.audio = self.r.listen(source,timeout=timeout)
            except sr.WaitTimeoutError:
                if DEBUG:
                    print("[Error] Listening timeout occured!")
                self.listen(recalibrate=recalibrate,CalibrateDuration=CAL_DURATION,startSpeakingSound=startSpeakingSound,timeout=timeout)
    
    def recognize(self,language="en-IN",offlineMode=False):
        success = True
        try:
            if offlineMode:
                self.out = self.r.recognize_sphinx(self.audio).strip()
            else:
                self.out = self.r.recognize_google_cloud(self.audio, credentials_json=self.credData, language=language).strip()
        except sr.RequestError:
            print("[Error] RequestError: API Unavailable/Unreachble. Check Connectivity/Credentials!")
            self.out = "Speech API is not available at this time."
            success = False
        except sr.UnknownValueError:
            print("[Error] UnknownValueError: API could not recognize the audio!")
            self.out = getRandomPhrase(UnknownValueErrorPhrases)
            success = False
        except Exception as e:
            print("[Error] Unknown exception: %s" % e)
            self.out = "Unknown Exception Occured: %s" % e
            success = False
        if DEBUG:
            print("[+] STT Output: %s" % self.out)
        return self.out, success

    def listenAndRecognize(self,recalibrate=True,CalibrateDuration=CAL_DURATION,language="en-IN",enableSound=True,timeout=None):
        self.listen(recalibrate=recalibrate,CalibrateDuration=CalibrateDuration,timeout=timeout,startSpeakingSound=enableSound)
        return self.recognize(language=language,offlineMode=False)

    def listenAndRecognizeOffline(self,recalibrate=True,CalibrateDuration=CAL_DURATION,language="en-IN",enableSound=False,timeout=None):
        self.listen(recalibrate=recalibrate,CalibrateDuration=CalibrateDuration,startSpeakingSound=enableSound,timeout=timeout)
        return self.recognize(language=language,offlineMode=True)