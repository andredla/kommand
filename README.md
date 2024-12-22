# Kommand

:. Kde plasma 5 plasmoid

Allows you to register voice commands to execute commands.<br/>
Tested on Linux, Kubuntu KDE plasma 5.

# Dependencies
- Paplay is used to play the sound
- Python 3
- speech_recognition package, version used SpeechRecognition 3.10.4

# Instalation guide
- Unzip the file
- Copy the folder to ~/.local/share/plasma/plasmoids/
- Then restart session
- Once it is installed it will appear under the system tray as Kommand

# Configuration
- Inside system tray under Kommand click on plasmoid configuration button
- Select the language you want
- under Command, click on configure
- Add a command word
- Click on add button
- Configure the line
- Save
- If you want do the same steps for terminal

# Images

![alt text](https://raw.githubusercontent.com/andredla/kommand/main/KommandConfig.png)

![alt text](https://raw.githubusercontent.com/andredla/kommand/main/Kommand.png)
  
# How it works
When you launch the Kommand icon inside the system tray, you wait for a sound and it will be listening for the Command, then you say the word you configure inside the Command field followed by the Word field and wait, then the system will run the Execute field and say the Talk field. If you say something that not match with any command, nothing will happend and the sound will play again and wait for the next command, the output of the text you speak will appear at KDE Klipboard. 
