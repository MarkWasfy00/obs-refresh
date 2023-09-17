import obsws_python as obs
import schedule
import time
import toml
import sys


data = toml.load("./config.toml")

REFRESH_SOURCE_NAME = data["settings"]["source_name"]
REFRESH_CYCLE = data["settings"]["refresh_time"]
OBS_HOST = data["obs"]["host"]
OBS_PORT = data["obs"]["port"]
OBS_PASS = data["obs"]["password"]
CONNECTION = False

class Obs:
    HOST = OBS_HOST
    PORT = OBS_PORT
    PASSWORD = OBS_PASS

    
    def __init__(self):
        self.cl = obs.ReqClient(host=self.HOST, port=self.PORT, password=self.PASSWORD)

    def refresh_media_source(self):
        global CONNECTION
        if CONNECTION:
            try:
                self.cl.set_input_settings(REFRESH_SOURCE_NAME, {},True)
                print("media source refreshed!")
            except:
                print("failed to refresh...")
                CONNECTION = False
                sys.exit()

while not CONNECTION:
    try:
        obs = Obs()
        schedule.every(REFRESH_CYCLE).minutes.do(obs.refresh_media_source)
        CONNECTION = True
        print("script running...")
    except:
        print("Please open obs")
        print("Retrying again after 10 seconds")
        time.sleep(10)

while True:
    schedule.run_pending()
    time.sleep(1)