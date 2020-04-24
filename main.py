
from globalVariables import *
import speakerClass
import recognizerClass
import actionClass

agent = actionClass.florenceActions()
agent.getLocation()
agent.getWeather()

'''
speaker = speakerClass.florenceTalks(gender='female',rate=165)
speaker.talk("The speech recognition service will shortly begin after this.")

recognizer = recognizerClass.florenceListens(CredFilePath=CRED_FILE)
stt = recognizer.listenAndRecognize()
speaker.talk(stt)
'''