
from apiKeys import *
import random
from playsound import playsound
import threading
import os
import time

# Variables - Tunable params
VOICE_GENDER = "female"
VOICE_RATE = 165

# Microphone Tunable params
CAL_DURATION = 1        # Seconds
PAUSE_THRESH = 0.8      # Seconds
DAMPING_RATIO = 0.7     # Default 0.15
ENERGY_RATIO = 15        # Default 1.5

# Strings - Mostly paths
CRED_FILE = "Florence-5acbc25bc627.json"
USER_CONF_FILE = "user.ini"
START_SPEAKING_SOUND = "sounds/start_speaking.mp3"

# Bools - Control toggles
VERSION = "1.00a"
AUTHOR = "Pranjal Joshi"
DEBUG = True
EN_START_SPEAKING_SOUND = True
STREAMING_LISTEN_TIMEOUT = 5    # Seconds

VLC_STATE_ENDED = 6             # VLC get_state() codes

# Phrases

InitiateWords = [
    "hey","hi","high","i","oh","hello","there","buddy","florence","lawrence"
]

FalseAlarmPhrases = [
    "Okay, False Alarm!",
    "Got it.",
    "Okay!",
    "Standing By",
    "No problem, call me when you need me!",
    "Sure, I will go back to the sleep then.",
    "Sorry, My bad!"
]

InitiatePharases = [
    "At your service!",
    "Yes Boss?",
    "Yes Sir!",
    "How can I help you?",
    "Hello. What can I do for you?",
    "Hey. Do you need something?",
    "I am here for you.",
    "I am listening. Go ahead!"
]

PositiveWords = [
    "yes","yep","yeh","yeah","obviously","indeed","ok","okay","tell me","i do","sure","why not"
]

NegativeWords = [
    "no","nop","nope","i don't","don't","not","never"
]

QuestionStopWords = [
    "search","find","from","google","wiki","wikipedia","tell","info","the","about","for",
    "summary","short","in","answer","define","what","where","is","was","were","when","who","how"
]

StreamStopWords = [
    "youtube","play","show","stream","watch","from","on"
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

ConfusedPhrases = [
    "Please tell me again.",
    "Sorry, I don't understand what you just said!",
    "I beg your pardon!",
    "I missed what you said!"
]

YesNoQuestionPhrases = [
    "Would you like to ",
    "Do you want to ",
    "Can I help you to",
    "Is it okay to "
    "Do you wish to "
]

DontKnowPhrases = [
    "Sorry, but I don't know the answer for this.",
    "Right now I can't give you the answer of this."
    "Actually, I don't know!",
    "I still need to learn about many things and this is one of them.",
    "Sir, I don't have any information about this.",
    "Even I also need to know more about this!",
    "I am unable to understand.",
    "I can't figure it out"
]

NetworkErrorPhrases = [
    "Sorry, but I could not connect to the network.",
    "I am unable to connect to the service at this moment",
    "I am trying to connect but internet is not working.",
    "As internet is not working, I could not answer this.",
    "Well, something went wrong with the network connectivity.",
    "I can't figure it out due to network issues",
    "I'm sorry but it seems like your network is down at this moment."
]

ProcessingPhrases = [
    "Processing. Please wait!",
    "Okay, I'm working on it.",
    "Sir, just a moment while i figure this out.",
    "Searching the internet for you now!",
    "I'm on it. Give me a second.",
    "Searching for your question.",
    "Please wait while I'm looking for the answer."
]

# Helper methods

def clearScreen():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

def getRandomPhrase(listName):
    return listName[random.randint(0,len(listName)-1)]

def removeStopWords(query):
    queryWords = query.lower().split()
    for qw in queryWords:
        for w in QuestionStopWords:
            if w == qw:
                query = query.replace(qw,'')
    return query

def removeStreamingWords(query):
    queryWords = query.lower().split()
    for qw in queryWords:
        for w in StreamStopWords:
            if w == qw:
                query = query.replace(qw,'')
    return query

def startingSpeakingSoundThread():
    playsound(START_SPEAKING_SOUND)

def playStartSpeakingSound():
    threading.Thread(target=startingSpeakingSoundThread).start()

def isWordInQuery(query,wordList):
    query = query.lower()
    for w in wordList:
        if w.lower() in query:
            return True
    return False

def getCurrentTime(ampm=True):
    if ampm:
        return time.strftime("%I:%M %p",time.localtime())
    else:
        return time.strftime("%H:%M %p",time.localtime())