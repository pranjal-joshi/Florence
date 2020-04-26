
from globalVariables import *
import speakerClass
import recognizerClass
import actionClass

clearScreen()
print("[+] Project Florence - A Python-based virtual assistant")
print("[+] Author: %s" % AUTHOR)
print("[+] Version: %s\n" % VERSION)

speaker = speakerClass.florenceTalks(gender='female',rate=165)
action = actionClass.florenceActions()
recognizer = recognizerClass.florenceListens(CredFilePath=CRED_FILE)

speaker.talk("Welcome!")

if __name__ == "__main__":
    while True:
        print("LOOPIN....")
        fromMic, success = recognizer.listenAndRecognizeOffline(enableSound=False)
        action.checkInitiateWord(fromMic, action.initUserInteraction)