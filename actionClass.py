
from globalVariables import *
import speakerClass
import recognizerClass
from configparser import ConfigParser
import pyowm

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

    def getLocation(self):
        self.speaker.talk(getQuestionPhrase() + "your current location? Only name of the place is enough for now!")
        input, success = self.recognizer.listenAndRecognize()
        if success:
            self.config.read(USER_CONF_FILE)
            if not self.config.has_section('user_data'):
                self.config.add_section('user_data')
            self.config.set('user_data','location',input)
            with open(USER_CONF_FILE, 'w') as f:
                self.config.write(f)
            self.speaker.talk(getSavingPhrase())
        else:
            self.speaker.talk("Sorry but I don't understand.")

    def getWeather(self):
        self.config.read(USER_CONF_FILE)
        loc = self.config.get('user_data','location')
        owm = pyowm.OWM(OWM_API_KEY)
        observation = owm.weather_at_place(loc)
        weather = observation.get_weather()
        fc = owm.three_hours_forecast(loc)
        rain_prob = fc.will_have_rain()
        print(weather.get_temperature(unit='celsius')['temp'])
        print(weather.get_detailed_status())
        print(observation.get_location().get_name())
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
