from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from actions import get_response_time
from prompts import system_promt
from json_helpers import extract_json
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

available_actions={
    "get_response_time": get_response_time
}

user_prompt="what is the response time for google.com"

message=[
    {"role": "system","content": system_promt},
    {"role": "user","content": user_prompt}
]

turn_count=1
max_turn=5

while turn_count<max_turn:
    print(f"Loop: {turn_count}")
    print("---------------------------")
    turn_count+=1
    response=generate_response(llm,message)
    print(response)
    json_function=extract_json(response)
    if json_function:
        function_name=json_function[0]['function_name']
        function_parms=json_function[0]['function_parms']
        if function_name not in available_actions:
            raise Exception(f"Unknown action: {function_name}: {function_parms}")
        print(f" -- running {function_name} {function_parms}")
        action_function=available_actions[function_name]
        result=action_function(**function_parms)
        function_result_message=f"Action_Response: {result}"
        print(function_result_message)
    else:
        break

