from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from actions import gen_movie_script,gen_audio,sentence_split
from prompts import system_prompt
load_dotenv()

#instance
llm=ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-70b-versatile"
)

def generate_response(llm,message):
    response=llm.invoke(message)
    return response.content

user_prompt=input()

message=[
    {"role": "system","content": system_prompt},
    {"role": "user","content": gen_movie_script(user_prompt)}
]
msg=generate_response(llm,message)
gen_audio(user_prompt)
split_msg=sentence_split(msg)
with open("split_output.txt", "w") as file:
    for word in split_msg:
        file.write(word + "\n")
