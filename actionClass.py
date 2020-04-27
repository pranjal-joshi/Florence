
from globalVariables import *
from apiKeys import *
import speakerClass
import recognizerClass
import multimediaClass
from configparser import ConfigParser
from configparser import Error as ConfigParserError
import pyowm
from pyowm.exceptions import api_response_error, api_call_error
import wikipedia as wiki
import email
import imaplib
import base64

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
        self.media = multimediaClass.florenceMultimedia()
    
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
                query = query.lower()
                if isWordInQuery(query,['wiki','wikipedia','summary','find','search','define','tell']):
                    self.speaker.talk(self.getWikiInfo(query))
                elif isWordInQuery(query,['youtube','play','stream']):
                    self.handleYoutubeStream(query)
                elif isWordInQuery(query,['weather','temperature']):
                    self.getWeather()
                elif isWordInQuery(query,['time','clock']):
                    self.speaker.talk("Right now its " + getCurrentTime())
                elif isWordInQuery(query,['false','nothing']):
                    self.speaker.talk(getRandomPhrase(FalseAlarmPhrases))
                elif isWordInQuery(query,['mail','inbox']):
                    self.checkGmail()
                else:
                    self.speaker.talk(self.getWikiInfo(query))
                    #self.speaker.talk(getRandomPhrase(DontKnowPhrases))
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

    def getWikiInfo(self, query):
        self.speaker.talk(getRandomPhrase(ProcessingPhrases))
        try:
            query = removeStopWords(query)
            return wiki.summary(query,sentences=2)
        except wiki.exceptions.DisambiguationError as e:
            e = str(e)
            e = e.split('\n')
            resp = "Your question seems ambiguous as the same keyword is applicable for "
            try:
                resp += e[1] + " "
                resp += e[2] + " "
                resp += e[3] + " "
            except IndexError:
                pass
            resp += "etc."
            return resp
        except:
            return getRandomPhrase(NetworkErrorPhrases)

    def handleYoutubeStream(self,query):
        self.speaker.talk(getRandomPhrase(ProcessingPhrases))
        url,success = self.media.youtubeSearch(query)
        if success:
            status,success2 = self.media.youtubeStreamAudio(url)
            if success2:
                isStreaming = True
                while isStreaming:
                    try:
                        fromMic, success = self.recognizer.listenAndRecognize(enableSound=False,timeout=STREAMING_LISTEN_TIMEOUT)
                        fromMic = fromMic.lower()
                        if isWordInQuery(fromMic,['stop','of','shut']):
                            self.media.youtubeStreamControl('stop')
                            isStreaming = False
                            self.speaker.talk("Okay, I'm stopping the music streaming service for you!")
                        elif isWordInQuery(fromMic,['pause','old','resume','play','again','continue','start']):
                            self.media.youtubeStreamControl('toggle')
                            self.speaker.talk("Okay!")
                        if self.media.player.get_state() == VLC_STATE_ENDED:
                            break
                    except Exception as e:
                        print(e)
                isStreaming = False
            else:
                getRandomPhrase(NetworkErrorPhrases)
        else:
            getRandomPhrase(NetworkErrorPhrases)

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
            cloud_prob = fc.will_have_clouds()
            cloud_phrase = "no chances"
            if cloud_prob:
                cloud_phrase = "chances"
            self.speaker.talk(
                "Right now, it is "
                + getCurrentTime()
                + ". The current temperature outside is "
                + str(round(weather.get_temperature(unit='celsius')['temp']))
                + " degree celsius. It is expected that today we will have a "
                + weather.get_detailed_status() + ". Also there are " + cloud_phrase
                + " of clouds up there. That's all for now."
                )
        except (api_response_error.NotFoundError, ConfigParserError):
            self.speaker.talk("The system API could not found weather reports for your location. Please correct the location by changing user configuration.")
            self.getLocation()
        except Exception as e:
            raise e
            self.speaker.talk(getRandomPhrase(NetworkErrorPhrases))

    def checkGmail(self,user=GMAIL_USER,passwd=GMAIL_PASS):
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(user,passwd)
        mail.select('inbox')
        result, data = mail.search(None,'(UNSEEN)')
        id_list = data[0].split()
        latest = id_list[-1]
        result, data = mail.fetch(latest,'(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                sub = msg['subject']
                sender = msg['from']
                print("From: " + sender)
                print("Subject: " + sub)
