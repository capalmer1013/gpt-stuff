import json
import os
import time

import openai
from rich.console import Console
# https://rich.readthedocs.io/en/latest/style.html

console = Console()
openai.api_key = os.environ["OPENAI_API_KEY"]

messages = [
    {
    "role": "system", 
    # "content": "You are a helpful assistant."
    # "content": "You are a story telling ai assistant."
    "content": "You are career advice assistant."
    },
]

with open(str(int(time.time()*100)) + ".json", "w") as f:
    while True:
        print()
        user_input = input(">>>")
        if user_input.lower() == "q":
            break
        message = {"role": "user", "content": user_input}
        messages.append(message)
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
       
        message = {"role": "assistant", "content": completion.choices[0].message.content}
        messages.append(message)
        print()
        console.print("CHAT >", style="color(6)")
        console.print(completion.choices[0].message.content)
    
    json.dump(messages, f)
        
