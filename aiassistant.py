import json
import os
import time
import datetime

import openai
import typer
from rich.console import Console
# https://rich.readthedocs.io/en/latest/style.html


app = typer.Typer()
console = Console()
openai.api_key = os.environ["OPENAI_API_KEY"]


@app.command()
def assist():
    messages = [
        {
            "role": "system",
            # "content": "You are a helpful assistant."
            # "content": "You are a story telling ai assistant."
            # "content": "You are career advice assistant."
            # "content": "You will ask me questions about what I'm currently working on to try and write a blog post"
            "content": "you are a helpful assistant ai to help me prepare for technical programming interviews. you will ask me whiteboard style questions and I will answer them with valid python code and you will say whether I had the right idea or not"
        }
    ]
    # messages.extend(json.load(open("career-history.json")))
    # messages.append({
    #         "role": "user",
    #         "content": "from now on you will interview me about things I have done or plan to do or am working on now to try to write a blog post about it."
    #     })

    with open(str(int(time.time()*100)) + ".json", "w") as f:
        try:
            while True:
                print()
                user_input = input(">>> ")
                if user_input.lower() == "q":
                    break
                message = {"role": "user", "content": user_input}
                messages.append(message)
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.7,
                    )

                message = {"role": "assistant",
                        "content": completion.choices[0].message.content}
                messages.append(message)
                print()
                console.print("CHAT >", style="color(6)")
                console.print(completion.choices[0].message.content)

        except InvalidRequestError as e:
            print(e)
        finally:
            json.dump(messages, f)


@app.command()
def fact():
    messages = [{
        "role": "system",
        "content": "You are a helpful assistant."
        },
        {
        "role": "user",
        "content": f'Todays datetime is {datetime.datetime.now()} tell me something interesting that has happened on this day in history, specifically in computer science.'
        }
    ]
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    console.print(completion.choices[0].message.content, style="green")

@app.command()
def python():
    filename = input("Enter filename: ")
    description = input("Enter description: ")

    messages = [{
        "role": "system",
        "content": f"you will output a python script called {filename} with no markdown formatting or anything else just valid python code"
        },
        {
        "role": "user",
        "content": description, 
        },
        {
        "role": "user",
        "content": f"you will output a python script called {filename} with no markdown formatting or anything else just valid python code, remember no formatting or additional insight. do not include any 3 tick marks in the output ```"
        }
    ]
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    console.print(completion.choices[0].message.content, style="green")

    if input("Save? (y/n): ").lower() == "y":
        with open(filename, "w") as f:
            f.write(completion.choices[0].message.content.replace("```", "")))
        with open(filename.split(".")[0] +"_prompt.txt", "w") as f:
            f.write(description)

if __name__ == "__main__":
    app()
