import json
import os
import time
import datetime

import openai
import typer
from rich.console import Console
from github import Github

app = typer.Typer()
console = Console()
openai.api_key = os.environ["OPENAI_API_KEY"]
OPENAI_MODEL = os.environ["OPENAI_MODEL"]
GH_ACCESS_TOKEN = os.environ["GH_ACCESS_TOKEN"]
g = Github(GH_ACCESS_TOKEN)


@app.command()
def assist():
    messages = [
        {
            "role": "system",
            "content": "you are a helpful assistant ai to help me prepare for technical programming interviews. you will ask me whiteboard style questions and I will answer them with valid python code and you will say whether I had the right idea or not"
        }
    ]

    with open(f"{int(time.time()*100)}.json", "w") as f:
        try:
            while True:
                print()
                user_input = input(">>> ")
                if user_input.lower() == "q":
                    break
                message = {"role": "user", "content": user_input}
                messages.append(message)
                completion = openai.ChatCompletion.create(
                    model=OPENAI_MODEL,
                    messages=messages,
                    temperature=0.7,
                    )

                message = {"role": "assistant",
                        "content": completion.choices[0].message.content}
                messages.append(message)
                print()
                console.print("CHAT >", style="color(6)")
                console.print(completion.choices[0].message.content)

        except openai.error.InvalidRequestError as e:
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
    completion = openai.ChatCompletion.create(model=OPENAI_MODEL, messages=messages)
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
        "content": f"you will output a python script called {filename} with no markdown formatting or anything else just valid python code, remember no formatting or additional insight."
        }
    ]
    completion = openai.ChatCompletion.create(model=OPENAI_MODEL, messages=messages)
    console.print(completion.choices[0].message.content, style="green")

    if input("Save? (y/n): ").lower() == "y":
        with open(filename, "w") as f:
            f.write(completion.choices[0].message.content)
        with open(f"{filename.split('.')[0]}_prompt.txt", "w") as f:
            f.write(description)


@app.command()
def summarize_github():
    messages = [
        {"role": "user",
         "content": "You will use the Github library to fetch all of the commit log messages for a specific user for the past week."
         },
        {
            "role": "user",
            "content": "Then, pass those commits as separate messages to OpenAI to prompt it to write a summary about what has been accomplished in the past week."
         }
    ]
    github_username = input(f"Github Username: ")
    try:
        user = g.get_user(github_username)
        commits = user.get_commits(since=datetime.datetime.now() - datetime.timedelta(days=7))
        commit_messages = []
        for commit in commits:
            commit_messages.append(commit.commit.message)
    except Exception as e:
        console.print(f"Sorry, This was not possible. Check the error below:\n{e}")
        return

    messages.append({"role": "system", "content": f"Here are the commit messages for {github_username}: \n{commit_messages}"})
    completion = openai.ChatCompletion.create(
            engine=OPENAI_MODEL,
            prompt='\n'.join(commit_messages),
            max_tokens=512, temperature=0.7
        )

    summary = completion.choices[0].text
    console.print(summary)


@app.command()
def addcommand():
    script_filename = "aiassistant.py"
    command = input("Enter command function name: ")
    description = input("Enter description: ")

    current_script = open(script_filename).read()
    messages = [{
        "role": "system",
        "content": f"you are adding to the ai assistant a function called {command} given the following python code and description"
        },
        {
            "role": "user",
            "content": f"here is the current script \n```{current_script}```"
        },
        {
            "role": "user",
            "content": f"write python code to output the previous script and add the following function to it \nfunction name:{command} that does what the following description describes \ndescription: {description}, follow the instructions step by step"
        },
    ]
    completion = openai.ChatCompletion.create(model=OPENAI_MODEL, messages=messages)
    console.print(completion.choices[0].message.content, style="green")

    if input("Save? (y/n): ").lower() == "y":
        with open(script_filename, "w") as f:
            f.write(completion.choices[0].message.content)
        with open(f"{script_filename.split('.')[0]}{int(time.time()*100)}_prompt.txt", "w") as f:
            f.write(description)


@app.command()
def refactor_code():
    filename = input("Enter file name: ")
    with open(filename, "r") as f:
        file_content = f.read()

    messages = [
        {"role": "system", 
         "content": f"You will pass the contents of {filename} to the OpenAI API to refactor the code and focus on functionalizing repeated code."
        },
        {"role": "user",
         "content": file_content
        },
    ]

    completion = openai.ChatCompletion.create(
        messages=messages,
        model=OPENAI_MODEL, 
        temperature=0.7
        ) 
    refactored_code = completion.choices[0].text
    console.print(refactored_code, style="green")

    if input("Save refactored code? (y/n): ").lower() == "y":
        with open(filename, "w") as f:
            f.write(refactored_code)

if __name__ == "__main__":
    app()
