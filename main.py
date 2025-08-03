from threading import Thread
from pathlib import Path
from playsound import playsound
import time
import os
import random
import json

fileName = "CurrentAudio"

scriptDirectory = str(Path(__file__).resolve())[:-7]

pathToAudio = scriptDirectory + fileName + '.mp3'
pathToTemp = scriptDirectory + 'oldRecordings/'
pathToJSON = scriptDirectory + 'allowed.json'
bot_config = scriptDirectory + "bot_config.json"

with open(bot_config, 'r') as file:
    loadedConfig = json.load(file)

randomSpeakMin = loadedConfig["Delay Between Bot Speaking and Trolling (in seconds)"][0]["randomSpeakMin"]
randomSpeakMax = loadedConfig["Delay Between Bot Speaking and Trolling (in seconds)"][0]["randomSpeakMax"]
trollMin = loadedConfig["Delay Between Bot Speaking and Trolling (in seconds)"][1]["trollMin"]
trollMax = loadedConfig["Delay Between Bot Speaking and Trolling (in seconds)"][1]["trollMax"]

count = 0

def AudioPlayer():
    print("Audio Player Active")
    while True:
        time.sleep(0.25)
            
        if Path(pathToAudio).is_file():
            try:
                print("Playing Audio")
                directoryList = os.listdir(pathToTemp)
                count = len(directoryList)

                playsound(pathToAudio)
                os.rename(pathToAudio, pathToTemp + str(count + 1) + '.mp3')
                count=0
            except:
                time.sleep(0.1)

def Timer(allowedName, minSeconds, maxSeconds):
    print(allowedName + " Timer Active")
    while True:
        try:
            with open(pathToJSON, 'r') as file:
                history = json.load(file)
            
                if history[allowedName][0]['Value'] == 'False':
                    randTime = random.randint(minSeconds, maxSeconds)
                    print(str(randTime) + " seconds left until the bot: " + allowedName)
                    time.sleep(randTime)

                    with open(pathToJSON, 'r') as file:
                        history = json.load(file)
                        
                    history[allowedName][0]['Value'] = 'True'

                    with open(pathToJSON, 'w') as file:
                        json.dump(history, file, indent=4)
                    
                    print('Wrote "True" to: ' + allowedName)
        except:
            time.sleep(0.01)

Thread(target=AudioPlayer, daemon=True).start()
Thread(target=Timer, args=("CanRandomlySpeak", randomSpeakMin, randomSpeakMax), daemon=True).start()
Thread(target=Timer, args=("CanTroll", trollMin, trollMax), daemon=True).start()

time.sleep(0.1)
input("Press enter to stop the program\n")