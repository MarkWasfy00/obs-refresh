import obsws_python as obs
import time
import toml
import datetime
import pytz

data = toml.load("./config.toml")

REFRESH_SOURCE_NAME = data["settings"]["source_name"]
REFRESH_CYCLE = data["settings"]["refresh_time"]
OBS_HOST = data["obs"]["host"]
OBS_PORT = data["obs"]["port"]
OBS_PASS = data["obs"]["password"]

CHECKED = False


class Obs:
    HOST = OBS_HOST
    PORT = OBS_PORT
    PASSWORD = OBS_PASS
    CONNECTION = False

    def start(self):
        self.cl = obs.ReqClient(host=self.HOST, port=self.PORT, password=self.PASSWORD)
        self.CONNECTION = True

    def refresh_media_source(self):
        self.cl.set_input_settings(REFRESH_SOURCE_NAME, {},True)
        print("media source refreshed!")
            

TP = Obs()

while True:
    if not TP.CONNECTION:
        try:
            TP.start()
            print("Connected")
        except:
            print("Failed to connect retrying after 10 secs")
            time.sleep(10)
    else:
        try:
            israel_tz = pytz.timezone("Israel")
            now = datetime.datetime.now(israel_tz)
            if (now.minute == 0 or now.minute == 30) and not CHECKED:
                TP.refresh_media_source()
                CHECKED = True
            elif (now.minute == 0 or now.minute == 30) and CHECKED:
                pass
            else:
                CHECKED = False
        except:
            TP.CONNECTION = False
            print("Connection dropped, trying again")
    time.sleep(1)
    