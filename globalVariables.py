
from apiKeys import *
import random
from playsound import playsound
import threading

VOICE_GENDER = "female"
VOICE_RATE = 165
DEBUG = True
CRED_FILE = "Florence-5acbc25bc627.json"
USER_CONF_FILE = "user.ini"
START_SPEAKING_SOUND = "sounds/start_speaking.mp3"

PositiveWords = [
    "yes","yep","yeh","yeah","obviously","indeed","ok","okay","tell me","i do","sure","why not"
]

NegativeWords = [
    "no","nop","nope","i don't","don't","not","never"
]

SavingPhrases = [
    "Thanks! I will remember it.",
    "Okay! Thanks for telling me.",
    "Done! That's saved.",
    "Cool! I will try to remember it.",
    "Good! Now I don't need to ask you this again.",
    "Okay sir! Saving your preferences.",
    "Affirmitive! Let me remember this!"
]

UnknownValueErrorPhrases = [
    "Sorry, I don't understand what you just said!",
    "I beg your pardon.",
    "Can you rephrase your question?",
    "I missed what you said!",
    "I could not find the meaning of it.",
    "Sorry, Please ask me the question again."
]

QuestionPhrases = [
    "Can you tell me ",
    "Can I ask you ",
    "May I know ",
    "Please tell me ",
    "I would like to know ",
    "I want to ask you about ",
    "I want to know ",
    "Please let me know about "
]

YesNoQuestionPhrases = [
    "Would you like to ",
    "Do you want to ",
    "Should I tell you ",
    "Do you wish to ",
]

def startingSpeakingSoundThread():
    playsound(START_SPEAKING_SOUND)

def playStartSpeakingSound():
    threading.Thread(target=startingSpeakingSoundThread).start()

def getYesNoQUestionPhrase():
    return YesNoQUestionPhrases[random.randint(0,len(YesNoQUestionPhrases)-1)]

def getSavingPhrase():
    return SavingPhrases[random.randint(0,len(SavingPhrases)-1)]

def getQuestionPhrase():
    return QuestionPhrases[random.randint(0,len(QuestionPhrases)-1)]

def getUnknownValueErrorPhrase():
    return UnknownValueErrorPhrases[random.randint(0,len(UnknownValueErrorPhrases)-1)]