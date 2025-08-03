from fish_audio_sdk import Session, TTSRequest, ReferenceAudio
from openai import OpenAI
from pathlib import Path
import json
import minescript
import sys
import random
import time

print("Running!")

scriptDirectory = str(Path(__file__).resolve())[:-7]
historyFile = scriptDirectory + "history.json"
allowedFile = scriptDirectory + "allowed.json"
bot_config = scriptDirectory + "bot_config.json"

with open(bot_config, 'r') as file:
    loadedConfig = json.load(file)

API_KEY_OpenAi = loadedConfig["API Keys"][0]["Open AI API KEY"]
API_KEY_FishAudio = loadedConfig["API Keys"][0]["Fish Audio API KEY"]
botTTS = loadedConfig["TTS Voice ID"][0]["Voice ID"]

PLAYERID = minescript.players(max_distance=1)[0].uuid

minimumEffectTime = loadedConfig["Troll Config"][0]["minimumEffectTime"]
maximumEffectTime = loadedConfig["Troll Config"][0]["maximumEffectTime"]
minimumEffectPower = loadedConfig["Troll Config"][0]["minimumEffectPower"]
maximumEffectPower = loadedConfig["Troll Config"][0]["maximumEffectPower"]

minimumTpAirDistance = loadedConfig["Troll Config"][1]["minimumTpAirDistance"]
maximumTpAirDistance = loadedConfig["Troll Config"][1]["maximumTpAirDistance"]

#Troll Commands

trollCommands = [
    "/effect give @a minecraft:",
    "/tp @a",
    "/execute at @a run fill ~-1 ~-1 ~-1 ~1 ~2 ~1 minecraft:",
    "/execute at @a run fill ~ ~ ~ ~ ~ ~ minecraft:lava",
    "/execute at @a run fill ~ ~7 ~ ~ ~7 ~ minecraft:anvil",
    "/execute at @a run summon minecraft:", # ~ ~ ~
    "/give @a minecraft:dirt 2304",
    "drop item"
]

possibleEffects = [
    "absorption ",
    "bad_omen ",
    "blindness ",
    "conduit_power ",
    "darkness ",
    "dolphins_grace ",
    "fire_resistance ",
    "glowing ",
    "haste ",
    "health_boost ",
    "hero_of_the_village ",
    "hunger ",
    "instant_damage ",
    "instant_health ",
    "invisibility ",
    "jump_boost ",
    "levitation ",
    "luck ",
    "mining_fatigue ",
    "nausea ",
    "night_vision ",
    "poison ",
    "regeneration ",
    "resistance ",
    "saturation ",
    "slowness ",
    "slow_falling ",
    "speed ",
    "strength ",
    "unluck ",
    "water_breathing ",
    "weakness ",
    "wither "
]

possibleFillBlocks = [
    "obsidian",
    "water",
    "cobweb",
    "powder_snow",
    "infested_stone",
    "sand",
    "stone",
    "ice",
    "gravel",
    "magma_block"
]

possibleSummonMobs = [
    "creeper",
    "silverfish",
    "phantom",
    "evoker",
    "blaze",
    "ghast",
    "warden",
    "vex",
    "witch",
    "elder_guardian",
    "hoglin",
    "ravager",
    "lightning_bolt"
]

client = OpenAI(api_key=API_KEY_OpenAi)
session = Session(API_KEY_FishAudio)

#Activation Related Variables

previousMessage = None
playerIsAlive = True
playerJustDied = False

# Random Troll Variables

randNumber = 0

with open(historyFile, 'r') as file:
    history = json.load(file)

currentHistory = None
newHistory = None

def CheckIfAllowed(type):
    try:
        with open(allowedFile, 'r') as file:
            allowedHistory = json.load(file)
        if allowedHistory[type][0]['Value'] == 'True':
            allowedHistory[type][0]['Value'] = 'False'
            with open(allowedFile, 'w') as file:
                json.dump(allowedHistory, file, indent=4)

            return True
        return False
    except: 
        time.sleep(1)
        CheckIfAllowed(type)

def GenerateTTS(name, generatedText):
    try:
        with open(str(name) + ".mp3", "wb") as f:
            for chunk in session.tts(TTSRequest(
                reference_id = botTTS,
                text = str(generatedText)
            )):
                f.write(chunk)
    except:
        time.sleep(1)
        GenerateTTS(name, generatedText)
        

def NewChat(message, sender):
    currentHistory = {
        "role": sender,
        "content": message
    }
    history["conversations"].append(currentHistory)

    response = client.responses.create(
        model="gpt-4.1-nano",
        input=str(history)
    )

    currentHistory = {
        "role": "GLaDOS",
        "content": response.output_text
    }
    history["conversations"].append(currentHistory)

    GenerateTTS(scriptDirectory + "CurrentAudio", response.output_text)

with minescript.EventQueue() as event_queue:
    event_queue.register_chat_listener()
    event_queue.register_damage_listener()
    event_queue.register_take_item_listener()
    event_queue.register_key_listener()
    while True:
        event = event_queue.get()
        if event.type == minescript.EventType.CHAT and event.message != previousMessage:
            previousMessage = event.message

            if playerJustDied == True: # Sends Death Message To GLaDOS
                NewChat(previousMessage, 'Server Message')
                playerJustDied = False

            if "-stop" in event.message.lower(): # Stop and Save Command
                print("Stopping...")
                with open(historyFile, 'w') as file:
                    json.dump(history, file, indent=4)
                sys.exit()
            elif "made the advancement" in event.message.lower() or "reached the goal" in event.message.lower() or "completed the challenge" in event.message.lower():
                NewChat(previousMessage, 'Server Message')
            elif "<" in event.message.lower() and ">" in event.message.lower(): # Player sends chat message
                NewChat(previousMessage, 'Player')
  
        if event.type == minescript.EventType.DAMAGE:
            if event.entity_uuid == PLAYERID and CheckIfAllowed("CanRandomlySpeak"): 
                if event.source == "mob":
                    mobName = minescript.entities(uuid=event.cause_uuid)[0].name
                    
                    NewChat("Player has taken damage(not killed) from: " + mobName, 'Server Message')
                else:
                    NewChat("Player has taken damage(not killed) from: " + event.source, 'Server Message')

            for x in range(100):
                if playerIsAlive == True and minescript.player_health() <= 0:
                    playerIsAlive = False
                    playerJustDied = True
                        
                    while playerIsAlive == False:
                        if minescript.player_health() > 0:
                            playerIsAlive = True
        
        if event.type == minescript.EventType.TAKE_ITEM and CheckIfAllowed("CanRandomlySpeak"): 
            itemName = event.item.name
            itemAmount = event.amount

            NewChat("Player has picked up " + str(itemAmount) + " " + itemName + "(s)", 'Server Message')
        
        if event.type == minescript.EventType.KEY and CheckIfAllowed("CanTroll"):
            
            randNumber = random.randint(1, len(trollCommands)) - 1
            pickedTroll = trollCommands[randNumber]
            if "effect" in pickedTroll:
                randNumber = random.randint(1, len(possibleEffects)) -1
                pickedEffect = possibleEffects[randNumber]

                randEffectTime = random.randint(minimumEffectTime, maximumEffectTime)
                randEffectPower = random.randint(minimumEffectPower, maximumEffectPower)

                command = pickedTroll + pickedEffect + str(randEffectTime) + " " + str(randEffectPower)
            elif "tp" in pickedTroll:
                randX = str(random.randint(minimumTpAirDistance, maximumTpAirDistance))
                randY = str(random.randint(minimumTpAirDistance, maximumTpAirDistance))
                randZ = str(random.randint(minimumTpAirDistance, maximumTpAirDistance))

                location = " ~" + randX + " ~" + randY + " ~" + randZ

                command = pickedTroll + location
            elif pickedTroll == "/execute at @a run fill ~-1 ~-1 ~-1 ~1 ~2 ~1 minecraft:":
                randNumber = random.randint(1, len(possibleFillBlocks)) -1
                pickedFillBlock = possibleFillBlocks[randNumber]

                command = pickedTroll + pickedFillBlock
            elif pickedTroll == "/execute at @a run summon minecraft:":
                randNumber = random.randint(1, len(possibleSummonMobs)) -1
                pickedSummonMob = possibleSummonMobs[randNumber]

                command = pickedTroll + pickedSummonMob + " ~ ~ ~"
            elif pickedTroll == "drop item":
                command = "Forced player to drop the item in their hand"
                NewChat(command, "GLaDOS used a command on player")

                minescript.player_press_drop(True)
                minescript.player_press_drop(False)
                continue
            else: 
                command = pickedTroll
            try:
                NewChat(command, "GLaDOS used a command on player")
                minescript.execute(command)
            except:
                print("Error: ", command)
        
