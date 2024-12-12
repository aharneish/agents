from gtts import gTTS

def gen_movie_script(msg):
    prompt_temp=f"""
    You are a expert movie script writer Your job is to write a short movie script which is 2 minutes long for the given scenario.
    the scenario is {msg}
"""
    return prompt_temp

def gen_audio(msg):
    gttsLang='en'
    replyObj=gTTS(text=msg,lang=gttsLang,slow=False)
    replyObj.save(f'Movie_audio_{msg[:10]}.mp3')

def sentence_split(msg):
    mess=msg.split('\n')
    return mess
