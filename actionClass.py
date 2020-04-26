
from globalVariables import *
import speakerClass
import recognizerClass
from configparser import ConfigParser
from configparser import Error as ConfigParserError
import pyowm
from pyowm.exceptions import api_response_error, api_call_error

class florenceActions:

    def __init__(self):
        try:
            self.config = ConfigParser()
            if DEBUG:
                print("[+] Initializing florenceActions class...")
            print("[+] Loading %s config file..." % USER_CONF_FILE)
            try:
                self.config.read(USER_CONF_FILE)
            except Exception as e:
                raise e
        except:
            print("[Error] Failed to access exisiting user config file: %s" % USER_CONF_FILE)
            print("[+] Creating new user config file: %s" % USER_CONF_FILE)
            self.config.read(USER_CONF_FILE)
            if not self.config.has_section('user_data'):
                self.config.add_section('user_data')
            self.config.set('user_data','key','val')
            with open(USER_CONF_FILE, 'w') as f:
                self.config.write(f)
        self.speaker = speakerClass.florenceTalks(gender=VOICE_GENDER, rate=VOICE_RATE)
        self.recognizer = recognizerClass.florenceListens(CredFilePath=CRED_FILE)
    
    def checkInitiateWord(self, input, onInitMethod):
        input = input.lower()
        input = input.split()
        for word in input:
            if word in InitiateWords:
                if DEBUG:
                    print("[+]Captured an Initiate Word. Triggering interactive mode..")
                self.speaker.talk(getRandomPhrase(InitiatePharases))
                onInitMethod()

    def decisionMaking(self,query,success):
        if DEBUG:
            print("[+] Decision Maker Query: %s" % str(query))
        if success:
            try:
                query = str(query.lower())
                query = query.split()
                if "weather" in query or "temperature" in query:
                    self.getWeather()
                elif "false" in query or "nothing" in query:
                    self.speaker.talk(getRandomPhrase(FalseAlarmPhrases))
                else:
                    self.speaker.talk(getRandomPhrase(DontKnowPhrases))
            except Exception as e:
                self.speaker.talk("Sorry, but following exception occured while parsing your query. " + str(e))
                raise e
        else:
            self.speaker.talk(query)

    def initUserInteraction(self):
        query,success = self.recognizer.listenAndRecognize()
        self.decisionMaking(query,success)

    def askYesNoQuestion(self,text):
        self.speaker.talk(text)
        input, success = self.recognizer.listenAndRecognizeOffline()
        inputList = input.split()
        PositiveCount, NegativeCount = 0,0
        for word in inputList:
            word = word.lower()
            if word in PositiveWords:
                PositiveCount += 1
            elif word in NegativeWords:
                NegativeCount += 1
        if PositiveCount > NegativeCount:
            return 1
        elif NegativeCount > PositiveCount:
            return -1
        else:
            self.speaker.talk(getRandomPhrase(ConfusedPhrases))
            return self.askYesNoQuestion(text)

    def getLocation(self):
        self.speaker.talk(getRandomPhrase(QuestionPhrases) + "your current location? Only name of the place is enough for now!")
        input, success = self.recognizer.listenAndRecognize()
        if success:
            self.config.read(USER_CONF_FILE)
            if not self.config.has_section('user_data'):
                self.config.add_section('user_data')
            self.config.set('user_data','location',input)
            with open(USER_CONF_FILE, 'w') as f:
                self.config.write(f)
            self.speaker.talk(getRandomPhrase(SavingPhrases))
        else:
            self.speaker.talk("Sorry but I don't understand.")

    def getWeather(self):
        try:
            self.config.read(USER_CONF_FILE)
            loc = self.config.get('user_data','location')
            owm = pyowm.OWM(OWM_API_KEY)
            observation = owm.weather_at_place(loc)
            weather = observation.get_weather()
            fc = owm.three_hours_forecast(loc)
            rain_prob = fc.will_have_rain()
            rain_phrase = "no chances"
            if rain_prob:
                rain_phrase = "chances"
            self.speaker.talk(
                "Current temperature outside is "
                + str(round(weather.get_temperature(unit='celsius')['temp']))
                + " degree celsius. It is expected that today we will have a "
                + weather.get_detailed_status() + ". Also there are " + rain_phrase
                + " of rain. That's all for now."
                )
        except (api_response_error.NotFoundError, ConfigParserError):
            self.speaker.talk("The system API could not found weather reports for your location. Please correct the location by changing user configuration.")
            self.getLocation()
        except Exception as e:
            raise e
            self.speaker.talk("The system is not able to connect to the weather service. Please check your network.")

