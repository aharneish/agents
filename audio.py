from gtts import gTTS
import os

file_path='./split_output.txt'
with open(file_path, 'r') as file:
    file_content = file.read()

gttsLang='en'
replyObj=gTTS(text=file_content,lang=gttsLang,slow=True)
replyObj.save(f'Movie_audio.mp3')