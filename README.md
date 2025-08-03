
# GLaDOS Minecraft AI Bot

By using OpenAI, Fish Audio, and Minescript, this GLaDOS look alike can comment on the players game, talk to the player through game chat, and grief them at random intervals.

**IMPORTANT:** This bot requires a API Key from OpenAI and Fish Audio, if you don't have one you won't be able to use this bot. Your OpenAI account will also need to be verified as this bot uses the gpt-4.1-nano LLM.

When it comes to the cost to run this bot on your own api, a majority of cost comes from Fish Audio. In total from the complete beginning of this project to the first upload to github here. I have spent $0.52 on Fish Audio and $1.49 on OpenAI but had I not ran multiple evaluations and used gpt-4.1-nano from the start, I'm estimating that OpenAI's cost would have been below $0.5 at max and I'm willing to say it could be way lower.




## Installation

As this is a small project, I have no clue as to whether or not this will run properly on macOS or linux however Windows will work for sure. As of now this project is running on the **1.21.5** version of Minecraft

### Windows

1. Make sure you have python and the following libraries installed on your device

    • fish_audio_sdk
    • openai
    • pathlib
    • json
    • sys
    • random
    • time
    • threading
    • os
    • playsound

2. Add [minescript](https://minescript.net/) as a mod to your Minecraft client. The easiest way I have found to do this is by adding it through a launcher like Curseforge or Modrinth.
3. Download the project as a zip and unzip the files
4. Move the unzipped files into the minescript folder which will be located in the same folder that the mods folder is located in.
5. Open the bot_config.json file and add your API Keys for OpenAI and FishAudio


**Note:** If you encounter a problem with the installation and or the program itself, please don't hesitate to open up a new issue, and I will try to respond whenever I have time.


## Usage

1. To start the program, first join a world that you want to run this on

2. Run the main.py script in the minescripts folder

3. Go back to minecraft and type into the chat: "\core"

4. GLaDOS should now be active in your game and should be able to comment aloud/mess with you

5. If you want to save all of the previous messages as a reference for GLaDOS in the future, type: "-stop" into the chat and it should save everything.

6. If you don't want to save all of the messages for that session, you can simply leave the game or type "\killjob -1" into the chat to terminate the process.



## Editing the Program

There are a few ways you can edit the program very easily without having to dive into the code itself. 

1. The easiest way will be in the bot_config.json folder where you can change nearly all of the config options that are used to determine certain behavior of the bot and the voice itself if you decide you don't want GLaDOS anymore.

2. The second way you can edit the program is by going into the history.json file. This file stores all of the previous conversations and instructions given to the bot which works as context for the LLM. Here you can change its complete behavior and train it to be something completely different than GLaDOS.

3. The third way you can edit the program is in the core.py file itself. There you will you a few lists that control the commands GLaDOS is able to send. I would be more careful here if you don't know what you are doing, but if something gets broken here, it won't hurt the bot at all to just replace the file with the default file.

**Note:** At  the bottom of the core.py file there is the code that handles all of the commands which should be able to take new commands if its in the same format as the conditions in the section.

