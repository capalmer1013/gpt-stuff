import json
import os
import time
import datetime

import typer
from rich.console import Console

from util import Chat, GithubWrapper

app = typer.Typer()
console = Console()


@app.command()
def assist():
    chat = Chat([("system", 
                  """you are a helpful assistant ai to help me prepare for technical programming interviews. 
                  you will ask me whiteboard style questions and I will answer them with valid python code. 
                  you will say whether I had the right idea or not""")])
    
    chat.cli()


@app.command()
def fact():
    chat = Chat([("system","You are a helpful assistant."),
                 ("user",
                  f"""Todays datetime is {datetime.datetime.now()} tell me something interesting that has happened on this day in history, 
                  specifically in computer science.""")])
    chat.single()



@app.command()
def python():
    filename = input("Enter filename: ")
    description = input("Enter description: ")

    chat = Chat([("system", f"you will output a python script called {filename} with no markdown formatting or anything else just valid python code"),
                    ("user", description),
                    ("user", f"you will output a python script called {filename} with no markdown formatting or anything else just valid python code, remember no formatting or additional insight.")
                ])
    chat.single()

    chat.save_prompt(description, f"{filename.split('.')[0]}{int(time.time()*100)}_prompt.txt")


@app.command()
def summarize_github():
    username = input(f"Github Username: ")
    commits = '\n'.join(GithubWrapper.get_commits(username))
    if commits:
        chat = Chat([
            ("user", "summary about what has been accomplished in the past week." ),
            ("system", f"Here are the commit messages for {username}: {commits}")
        ])

        chat.single()


@app.command()
def addcommand():
    script_filename = "aiassistant.py"
    command = input("Enter command function name: ")
    description = input("Enter description: ")

    current_script = open(script_filename).read()
    messages = generate_messages(
        ("system", f"you are adding to the ai assistant a function called {command} given the following python code and description"),
        ("user", f"here is the current script \n```{current_script}```"),
        (
            "user",
            f"write python code to output the previous script and add the following function to it \nfunction name:{command} that does what the following description describes \ndescription: {description}, follow the instructions step by step",
        ),
    )
    completion = openai.ChatCompletion.create(model=OPENAI_MODEL, messages=messages)
    print_response(completion.choices[0].message.content)

    if input("Save? (y/n): ").lower() == "y":
        save_response(completion.choices[0].message.content, script_filename)
        save_response(description, f"{script_filename.split('.')[0]}{int(time.time()*100)}_prompt.txt")


@app.command()
def refactor():
    filename = input("Enter file name: ")
    with open(filename, "r") as f:
        file_content = f.read()

    chat = Chat([
        ("system", f"You will pass the contents of {filename} to the OpenAI API to refactor the code and focus on functionalizing repeated code."),
        ("user", file_content)])

    chat.single()
    chat.save_prompt(file_content, filename)


if __name__ == "__main__":
    app()
