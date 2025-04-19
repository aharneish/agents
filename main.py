from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from actions import gen_movie_script, gen_audio, sentence_split
from prompts import system_prompt
from video_gen.generate_video import generate_video_from_textfile

load_dotenv()

# Instance
llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def generate_response(llm, message):
    response = llm.invoke(message)
    return response.content

user_prompt = input("Enter movie concept/idea: ")

message = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": gen_movie_script(user_prompt)}
]

msg = generate_response(llm, message)
gen_audio(user_prompt)
split_msg = sentence_split(msg)

with open("split_output.txt", "w", encoding="utf-8") as file:
    for line in split_msg:
        file.write(line + "\n")

# ✨ Video generation call
generate_video_from_textfile("split_output.txt", "generated_movie.mp4")